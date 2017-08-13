# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
from collections import Counter

from openerp import api, models, fields, _
from odoo.exceptions import Warning


class ScheduleReport(models.TransientModel):
    # class fields are defined here
    _name = 'schedule.report'

    current_date = fields.Date(
        default=fields.Date.context_today
    )
    threshold_date = fields.Date()
    categ_name = fields.Char()

    # # Data fields, used to browse report data
    categ_id = fields.Many2one(
        comodel_name='product.category',
    )
    line_ids = fields.One2many(
        comodel_name='schedule.report.line',
        inverse_name='report_id'
    )


class ScheduleReportLine(models.TransientModel):
    _name = 'schedule.report.line'

    report_id = fields.Many2one(
        comodel_name='schedule.report',
        ondelete='cascade',
        index=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        index=True,
    )
    categ_id = fields.Many2one(
        comodel_name='product.category',
    )

    product_name = fields.Char()
    categ_name = fields.Char()
    bal1 = fields.Float()
    in0 = fields.Float()
    out0 = fields.Float()
    in1 = fields.Float()
    out1 = fields.Float()
    in2 = fields.Float()  # first period in output
    out2 = fields.Float()
    bal2 = fields.Float()
    in3 = fields.Float()  # second period in output
    out3 = fields.Float()
    bal3 = fields.Float()
    in4 = fields.Float()  # third period in output
    out4 = fields.Float()
    bal4 = fields.Float()
    in5 = fields.Float()  # fourth period in output
    out5 = fields.Float()
    bal5 = fields.Float()
    in6 = fields.Float()  # fifth period in output
    out6 = fields.Float()
    bal6 = fields.Float()


class ShipmentScheduleReportCompute(models.TransientModel):
    # only methods are defined here
    _inherit = 'schedule.report'

    @api.multi
    def print_report(self):
        self.ensure_one()
        self.compute_data_for_report()
        report_name = 'stock_shipment_schedule_report.schedule_report'
        return self.env['report'].get_action(self, report_name)

    def _prepare_report_xlsx(self):
        self.ensure_one()
        return {
            'threshold_date': self.threshold_date,
            'categ_id': self.categ_id,
        }

    def _get_dates(self, threshold_date):
        res = {}
        res['current_date_local'] = fields.Datetime.context_timestamp(self, datetime.now())
        res['current_date_utc'] = datetime.now()
        threshold_date = datetime.strptime(threshold_date, '%Y-%m-%d')
        tz = pytz.timezone(self.env.user.tz) or pytz.utc
        threshold_date_local = tz.localize(threshold_date, is_dst=None)
        res['threshold_date_utc'] = threshold_date_local.astimezone(pytz.utc)
        return res

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

    def _get_line_title(self, cr, uid, periods, tz, context=None):
        line_title = []
        title_vals = {}
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
        line_title.append(title_vals)
        return line_title

    def _get_product_ids(self, category_id):
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
                location_id %s %s AND
                location_dest_id %s %s AND
                product_id IN %s AND
                state NOT IN ('done', 'cancel') AND
                m.date_expected >= %s AND
                m.date_expected < %s
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
                product_id IN %s AND
                order_id in (
                    SELECT
                        id
                    FROM
                        sale_order
                    WHERE
                        state = 'draft' AND
                        expected_date >= %s AND
                        expected_date < %s
                )
            GROUP BY product_id
            """ % (tuple(params))
        self.env.cr.execute(sql)
        qty_dict = self.env.cr.dictfetchall()
        for rec in qty_dict:
            res[rec['product_id']] = rec['sum']
        return res

    def _get_qty_data(self, products, periods, line_vals):
        res = []
        # # this conversion (instead of 'tuple(product_ids,)' is in case there is only one product)
        # param_prod_ids = str(product_ids).replace('[', '(').replace(']', ')')
        param_prod_ids = [p.id for p in products]
        # int_loc_ids = self.pool.get('stock.location').search(cr, uid, [
        #     ('usage', '=', 'internal')])
        locs = self.env['stock.location'].search([('usage', '=', 'internal')])
        loc_ids = [l.id for l in locs]
        i = 0
        for _ in xrange(7):
            date_from = "'" + str(periods[i]['start']) + "'"
            date_to = "'" + str(periods[i]['end']) + "'"
            # in_params = ['NOT IN', tuple(int_loc_ids, ), 'IN',
            #              tuple(int_loc_ids, ), param_prod_ids, date_from,
            #              date_to]
            in_params = ['NOT IN', tuple(loc_ids), 'IN', tuple(loc_ids),
                         tuple(param_prod_ids), date_from, date_to]
            out_params = ['IN', tuple(loc_ids, ), 'NOT IN',
                          tuple(loc_ids, ), tuple(param_prod_ids), date_from,
                          date_to]
            # dates4quote = self._get_dates4quote(periods[i])
            # quote_params = [param_prod_ids, dates4quote['start'],
            #                 dates4quote['end']]
            quote_params = [tuple(param_prod_ids), date_from, date_to]
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

    def _get_lines(self, periods, category_id):
        res = []
        line_vals = {}
        products = self._get_product_ids(category_id)
        # for prod in self.env['product.product'].browse(product_ids):
        for prod in products:
            line_vals[prod.id] = {
                'report_id': self.id,
                'product_id': prod.id,
                'product_name': prod.name,
                'categ_id': prod.categ_id.id,
                'categ_name': prod.categ_id.display_name,
                'bal1': prod.qty_available,
                'in0': 0.0,
                'out0': 0.0,
                'in1': 0.0,
                'out1': 0.0,
                'in2': 0.0,  # first period in output
                'out2': 0.0,
                'bal2': 0.0,
                'in3': 0.0,  # second period in output
                'out3': 0.0,
                'bal3': 0.0,
                'in4': 0.0,  # third period in output
                'out4': 0.0,
                'bal4': 0.0,
                'in5': 0.0,  # fourth period in output
                'out5': 0.0,
                'bal5': 0.0,
                'in6': 0.0,  # fifth period in output
                'out6': 0.0,
                'bal6': 0.0,
            }
        lines = self._get_qty_data(products, periods, line_vals)
        for line in lines:  # only append values (without key) to form the list
            for k, v in line.iteritems():
                res.append(v)
        res = sorted(res, key=lambda k: (k['categ_name'], k['product_name']))
        return res

    @api.multi
    def compute_data_for_report(self):
        self.ensure_one()
        threshold_date = self.threshold_date or False
        category_id = self.categ_id or False
        dates = self._get_dates(threshold_date)
        periods = self._get_periods(dates)
        lines = self._get_lines(periods, category_id)
        for line in lines:
            self.env['schedule.report.line'].create(line)
        self.refresh()
