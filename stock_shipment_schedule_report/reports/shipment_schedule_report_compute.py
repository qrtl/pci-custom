# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
from collections import Counter

from odoo import models, fields, api, _
from odoo.exceptions import Warning


class ShipmentScheduleReportCompute(models.TransientModel):
    # only methods are defined here
    _inherit = 'shipment.schedule.report'

    @api.multi
    def print_report(self):
        self.ensure_one()
        threshold_date = self.threshold_date or False
        category_id = self.categ_id or False
        website_published = self.website_published or False
        dates = self._get_dates(threshold_date)
        periods = self._get_periods(dates)
        self.write(self._get_header_periods(periods))
        lines = self._get_lines(periods, category_id, website_published)
        for line in lines:
            self.env['shipment.schedule.report.line'].create(line)
        self.refresh()
        report_name = 'stock_shipment_schedule_report.shipment_schedule_report'
        return self.env['report'].get_action(self, report_name)

    def _get_dates(self, threshold_date):
        tz = pytz.timezone(self.env.user.tz) or pytz.utc
        thres_date = datetime.strptime(threshold_date, '%Y-%m-%d')
        thres_date_local = tz.localize(thres_date, is_dst=None)
        thres_date_utc = thres_date_local.astimezone(pytz.utc)
        return {
            'current_date_local': fields.Datetime.context_timestamp(
                self, datetime.now()),
            'current_date_utc': datetime.now(),
            'threshold_date_utc': thres_date_utc
        }

    def _get_periods(self, dates):
        periods = {}
        current_date = dates['current_date_utc']
        threshold_date = dates['threshold_date_utc']
        i = 0
        for _ in xrange(7):
            if i == 0:  # for "Shipment on Hold" for the 1st period (period 2)
                start = current_date - relativedelta(years=100)
                end = current_date
            elif i == 1:  # for "Shipment" for the 1st period (period 2)
                start = current_date
                end = threshold_date + relativedelta(days=1)
            elif i == 2:
                start = threshold_date - relativedelta(years=100)
                end = threshold_date + relativedelta(days=1)
            else:
                start = end
                if not i == 6:
                    end = start + relativedelta(days=7)
                else:  # for the last period
                    end += relativedelta(years=100)
            periods[i] = {
                'start': start,
                'end': end,
            }
            i += 1
        return periods

    def _get_header_periods(self, periods):
        title_vals = {}
        tz = pytz.timezone(self.env.user.tz) or pytz.utc
        for p in periods:
            if p >= 2:  # period 0 and 1 are ignored
                if p == 2:
                    start = ''
                else:
                    start = datetime.strftime(
                        periods[p]['start'].astimezone(tz), '%Y-%m-%d')
                if p == 6:
                    end = ''
                else:
                    end = datetime.strftime(
                        periods[p]['end'].astimezone(tz) - relativedelta(
                            days=1), '%Y-%m-%d')
                title_vals['p' + `p`] = start + ' ~ ' + end
        return title_vals

    def _get_product_ids(self, category_id, website_published):
        domain = [
            ('sale_ok', '=', True),
            ('type', '=', 'product'),
            ('active', '=', True)
        ]
        # identify all categories under the selected category including itself
        if category_id:
            categs = [category_id]
            for categ in categs:
                if categ.child_id:
                    for child_categ in categ.child_id:
                        categs.append(child_categ) if child_categ not in \
                                                      categs else categs
            categ_ids = [categ.id for categ in categs]
            domain.append(('categ_id', 'in', categ_ids))
        if website_published:
            domain.append(('website_published', '=', True))
        prod_ids = self.env['product.product'].search(domain)
        if not prod_ids:
            raise Warning(_("There is no product to meet the condition (i.e. "
                            "'Saleable', 'Stockable' and belonging to the "
                            "selected Product Category or its offsprings)."))
        return prod_ids

    def _get_move_qty_data(self, params):
        res = {}
        sql = """
            SELECT
                m.product_id,
                SUM(m.product_qty / u.factor)
            FROM
                stock_move m
            LEFT JOIN
                product_uom u ON m.product_uom = u.id
            WHERE
                location_id %s (%s) AND
                location_dest_id %s (%s) AND
                product_id IN (%s) AND
                state NOT IN ('done', 'cancel') AND
                m.date_expected >= '%s' AND
                m.date_expected < '%s'
            GROUP BY
                product_id
            """ % (tuple(params))
        self.env.cr.execute(sql)
        qty_dict = self.env.cr.dictfetchall()
        for rec in qty_dict:
            res[rec['product_id']] = rec['sum']
        return res

    def _get_quote_qty_data(self, params):
        res = {}
        sql = """
            SELECT
                ol.product_id,
                SUM(ol.product_uom_qty / u.factor)
            FROM
                sale_order_line ol
            LEFT JOIN
                product_uom u ON ol.product_uom = u.id
            WHERE
                product_id IN (%s) AND
                order_id in (
                    SELECT
                        id
                    FROM
                        sale_order
                    WHERE
                        state = 'draft' AND
                        expected_date >= '%s' AND
                        expected_date < '%s'
                )
            GROUP BY product_id
            """ % (tuple(params))
        self.env.cr.execute(sql)
        qty_dict = self.env.cr.dictfetchall()
        for rec in qty_dict:
            res[rec['product_id']] = rec['sum']
        return res

    def _get_locs(self):
        loc_domain = [
            ('company_id', '=', self.env.user.company_id.id),
            ('usage', '=', 'internal'),
            ('active', '=', True)
        ]
        if self.limit_locs:
            loc_domain.append(('consider_qty', '=', True))
        return self.env['stock.location'].search(loc_domain)

    def _get_qty_data(self, products, periods, line_vals):
        res = []
        # convert tuples into strings to avoid sql error due to trailing comma
        # (,) in case there is only one id returned
        prod_ids = tuple([p.id for p in products])
        prod_ids_str = ', '.join(map(repr, prod_ids))
        loc_ids = tuple([l.id for l in self._get_locs()])
        loc_ids_str = ', '.join(map(repr, loc_ids))
        i = 0
        for _ in xrange(7):
            date_from = fields.Datetime.to_string(periods[i]['start'])
            date_to = fields.Datetime.to_string(periods[i]['end'])
            in_params = ['NOT IN', loc_ids_str, 'IN', loc_ids_str,
                         prod_ids_str, date_from, date_to]
            out_params = ['IN', loc_ids_str, 'NOT IN', loc_ids_str,
                          prod_ids_str, date_from, date_to]
            quote_params = [prod_ids_str, date_from, date_to]
            for type in ['in', 'out']:
                if type == 'in':
                    qty_data = self._get_move_qty_data(in_params)
                else:
                    move_qty_data = self._get_move_qty_data(out_params)
                    quote_qty_data = self._get_quote_qty_data(quote_params)
                    qty_data = dict(
                        Counter(move_qty_data) + Counter(quote_qty_data))
                for k, v in qty_data.iteritems():
                    line_vals[k][type + `i`] = v
            i += 1
        for prod in line_vals:
            i = 2  # start from period "2" (period until threshold date)
            for _ in xrange(5):
                line_vals[prod]['bal' + `i`] \
                    = line_vals[prod]['bal' + `i - 1`] + line_vals[prod][
                    'in' + `i`] - line_vals[prod]['out' + `i`]
                i += 1
        res.append(line_vals)
        return res

    def _get_qoh(self, prod):
        locs = self._get_locs()
        quants = self.env['stock.quant'].search(
            [('company_id', '=', self.env.user.company_id.id),
             ('product_id', '=', prod.id),
             ('location_id', 'in', [l.id for l in locs])]
        )
        return sum(q.qty for q in quants) if quants else 0.0

    def _get_lines(self, periods, category_id, website_published):
        res = []
        line_vals = {}
        products = self._get_product_ids(category_id, website_published)
        for prod in products:
            qoh = self._get_qoh(prod)
            line_vals[prod.id] = {
                'report_id': self.id,
                'product_id': prod.id,
                'product_name': prod.display_name,
                'categ_id': prod.categ_id.id,
                'categ_name': prod.categ_id.display_name,
                'bal1': qoh,
                'in0': 0.0, 'out0': 0.0,
                'in1': 0.0, 'out1': 0.0,
                'in2': 0.0, 'out2': 0.0, 'bal2': 0.0, # first period in output
                'in3': 0.0, 'out3': 0.0, 'bal3': 0.0, # second period in output
                'in4': 0.0, 'out4': 0.0, 'bal4': 0.0, # third period in output
                'in5': 0.0, 'out5': 0.0, 'bal5': 0.0, # fourth period in output
                'in6': 0.0, 'out6': 0.0, 'bal6': 0.0, # fifth period in output
            }
        lines = self._get_qty_data(products, periods, line_vals)
        for line in lines:  # only append values (without key) to form the list
            for k, v in line.iteritems():
                res.append(v)
        res = sorted(res, key=lambda k: (k['categ_name'], k['product_name']))
        return res
