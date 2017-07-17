# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    yearly_sales_history_ids = fields.One2many(
        'partner.yearly_sales',
        'partner_id',
        string = 'Yearly Sales',
        copy=False,
    )
    company_currency_id = fields.Many2one(
        'res.currency',
        related="company_id.currency_id",
        store=True,
        readonly=True,
        string="Company Currency",
    )

    @api.multi
    def _update_current_pricelist(self):
        self.ensure_one()
        today = fields.Date.context_today(self)
        last_year = fields.Date.to_string(
            fields.Date.from_string(today) + relativedelta(years=-1))
        hist_recs = self.yearly_sales_history_ids.filtered(
            lambda x: (x.start_date <= today and x.end_date >= today) or
                      (x.start_date <= last_year and x.end_date >= last_year)
        )
        amount = hist_recs.sorted(
            key=lambda r: r.amt_total)[-1].amt_total
        group = self.property_product_pricelist.pricelist_group_id
        if group:
            new_pricelist = self.env['product.pricelist'].search(
                [('pricelist_group_id', '=', group.id),
                 ('sale_threshold_amt', '<=', amount),
                 ('active', '=', True)],
                order='sale_threshold_amt desc', limit=1
            )
            if self.property_product_pricelist != new_pricelist:
                self.property_product_pricelist = new_pricelist
        return True

    def _get_customer_ids(self):
        partners = self.env['res.partner'].sudo().search(
            [('customer', '=', True),
             ('active', '=', True)]
        )
        return [p.id for p in partners]

    @api.multi
    def _update_partner_purchase_data(self, amount, date_start, date_end):
        self.ensure_one()
        history_rec = self.yearly_sales_history_ids.filtered(
            lambda x: x.end_date == date_end
        )[0]
        if history_rec:
            if history_rec.amt_computed != amount:
                history_rec.write({'amt_computed': amount})
        else:
            vals = {
                'partner_id': self.id,
                'start_date': date_start,
                'end_date': date_end,
                'amt_computed': amount,
            }
            self.env['partner.yearly_sales'].sudo().create(vals)

    @api.multi
    def reset_partner_pricelist(self, date_range, partner_id=False):
        date_start = date_range.date_start
        date_end = date_range.date_end
        if partner_id:
            partner_ids = tuple([partner_id.id])
        else:
            partner_ids = tuple(self._get_customer_ids())
        # FIXME identification of shipping charges
        self._cr.execute("""
            SELECT
                p.commercial_partner_id AS partner_id,
                SUM(base_amt) AS amount
            FROM
                sale_order_line sol
            JOIN
                sale_order so ON sol.order_id = so.id
            JOIN
                res_partner p ON so.partner_id = p.id
            WHERE
                sol.is_delivery IS FALSE AND
                sol.name NOT LIKE %s AND
                so.partner_id in %s AND
                so.state in ('sale', 'done') AND
                so.date_order_ctx >= %s AND
                so.date_order_ctx <= %s
            GROUP BY
                p.commercial_partner_id
            """, ('%Shipping Cost%',
                  partner_ids,
                  date_start,
                  date_end)
        )
        sales_data = self._cr.dictfetchall()
        for sales_dict in sales_data:
            partner = self.env['res.partner'].browse(sales_dict['partner_id'])
            if partner:
                partner._update_partner_purchase_data(
                    sales_dict['amount'], date_start, date_end)
                partner._update_current_pricelist()
        return True

    @api.multi
    def cron_reset_policy_pricelist(self):
        # FIXME add date_range
        partners = self.env['res.partner']\
            .sudo().search([('customer','=', True)])
        partners.reset_partner_pricelist()
        return True
