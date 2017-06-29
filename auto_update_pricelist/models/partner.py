# -*- coding: utf-8 -*-

from openerp import models, api, fields
from datetime import datetime


class ResPartner(models.Model):
    _inherit = "res.partner"

    yearly_purchase_total = fields.Float(
        string = 'Yearly Purchase',
        compute="_yearly_purchase_total",
        store=True,
    )
    sale_order_ids = fields.One2many(
        'sale.order',
        'partner_id',
        string = 'Sale Orders',
        copy=False,
    )
    yearly_sales_history_ids = fields.One2many(
        'partner.yearly_sales',
        'partner_id',
        string = 'Yearly Sales',
        readonly=True,
        copy=False,
    )
    company_currency_id = fields.Many2one(
        'res.currency',
        related="company_id.currency_id",
        store=True,
        string="Company Currency",
    )

    @api.model
    def _get_year_dates(self):
        start_date = datetime.now().date().replace(month=1, day=1)
        end_date = datetime.now().date().replace(month=12, day=31)
        return start_date, end_date

    @api.multi
    @api.depends(
        'yearly_sales_history_ids',
        'sale_order_ids',
        'sale_order_ids.state',
        'sale_order_ids.order_line',
        'sale_order_ids.order_line.price_total'
    )
    def _yearly_purchase_total(self):
        starting_day_of_current_year, ending_day_of_current_year = self._get_year_dates()
        for rec in self:
            if rec.id:
                self._cr.execute("""
                    SELECT
                        SUM(price_subtotal) as line_total,
                        line.currency_id
                    FROM
                        sale_order_line line
                    LEFT JOIN
                        sale_order so ON line.order_id = so.id
                    WHERE
                        line.is_delivery IS FALSE AND
                        so.partner_id=%s AND
                        so.state = 'sale' AND
                        to_char(so.date_order, 'YYYY-MM-DD')::date >= %s AND
                        to_char(so.date_order, 'YYYY-MM-DD')::date <= %s
                    GROUP BY
                        line.currency_id
                    """,
                    (rec.id, starting_day_of_current_year, ending_day_of_current_year)
                )
                sales_total = self._cr.dictfetchall()
                sales_total_amount = 0.0
                if sales_total:
                    for data in sales_total:
                        if data['currency_id'] != rec.company_currency_id.id:
                            current_currency = self.env['res.currency'].sudo().browse(data['currency_id'])
                            exchange_amt = current_currency.compute(data['line_total'], rec.company_currency_id)
                            sales_total_amount += exchange_amt
                        else:
                            sales_total_amount += data['line_total']
                rec.yearly_purchase_total = sales_total_amount

    @api.model
    def _prepare_yearly_sales_history_vals(self):
        starting_day_of_current_year, ending_day_of_current_year = self._get_year_dates()
        vals = {
            'partner_id': self.id,
            'start_date': starting_day_of_current_year,
            'end_date': ending_day_of_current_year,
            'sales_amount' : 0.0,
        }
        return vals

    @api.model
    def _update_currenct_pricelist(self):
        pricelist_policy = self.property_product_pricelist.product_pricelist_policy_id
        if pricelist_policy:
            available_pricelists = pricelist_policy.pricelist_ids
            if available_pricelists:
                available_pricelists = tuple(available_pricelists.ids)
                self._cr.execute("""
                    SELECT
                        id
                    FROM
                        product_pricelist
                    WHERE
                        id in %s AND
                        sale_threshold_amount < %s
                    ORDER BY
                        sale_threshold_amount desc
                    LIMIT 1
                """, (available_pricelists, self.yearly_purchase_total))
                new_pricelist = self._cr.dictfetchall()
                if new_pricelist:
                    self.property_product_pricelist = new_pricelist[0]['id']
        return True

    @api.multi
    def reset_partner_pricelist(self):
        for partner in self:
            default_pricelist = self.env['product.pricelist'].search([('is_default', '=', True)], limit=1)
            if default_pricelist:
                partner.property_product_pricelist = default_pricelist
            partner._update_currenct_pricelist()

            yearly_sales_ids = partner.yearly_sales_history_ids
            yearly_sales_ids = yearly_sales_ids.filtered(lambda y: y.sales_amount == 0.0).sorted(key='id', reverse=True)
            if yearly_sales_ids :
                yearly_sales_ids[0].write({'sales_amount': partner.yearly_purchase_total})
            vals = partner._prepare_yearly_sales_history_vals()
            self.env['partner.yearly_sales'].sudo().create(vals)
        return True

    @api.multi
    def cron_reset_policy_pricelist(self):
        partners = self.env['res.partner'].sudo().search([('customer','=', True)])
        partners.reset_partner_pricelist()
        return True

    @api.model
    def create(self, vals):
        if vals.get('customer', False):
            history_vals = self._prepare_yearly_sales_history_vals()
            vals.update({'yearly_sales_history_ids': [(0, 0, history_vals)]})
        return super(ResPartner, self).create(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: