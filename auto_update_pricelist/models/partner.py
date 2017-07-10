# -*- coding: utf-8 -*-

from openerp import models, api, fields


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
    def _get_year_dates(self, year):
        start_date = fields.Datetime.now().replace(month=1, day=1)
        start_date = start_date.replace(year=start_date.year-year)
        end_date = fields.Datetime.now().replace(month=12, day=31)
        end_date = end_date.replace(year=end_date.year-year)
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
        starting_day_of_current_year, ending_day_of_current_year = \
            self._get_year_dates(0)
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
                        line.name NOT LIKE %s AND
                        so.partner_id=%s AND
                        so.state = 'sale' AND
                        to_char(so.date_order, 'YYYY-MM-DD')::date >= %s AND
                        to_char(so.date_order, 'YYYY-MM-DD')::date <= %s
                    GROUP BY
                        line.currency_id
                    """, ('%Shipping Cost%',
                          rec.id,
                          starting_day_of_current_year,
                          ending_day_of_current_year)
                )
                sales_total = self._cr.dictfetchall()
                sales_total_amount = 0.0
                if sales_total:
                    for data in sales_total:
                        if data['currency_id'] != rec.company_currency_id.id:
                            current_currency = self.env['res.currency']\
                                .sudo().browse(data['currency_id'])
                            exchange_amt = current_currency.compute(
                                data['line_total'],
                                rec.company_currency_id
                            )
                            sales_total_amount += exchange_amt
                        else:
                            sales_total_amount += data['line_total']
                rec.yearly_purchase_total = sales_total_amount

    @api.model
    def _update_current_pricelist(self):
        amount = self.yearly_purchase_total
        last_year_start_day, last_year_end_day = self._get_year_dates(1)
        yearly_sales_ids = self.yearly_sales_history_ids
        yearly_sales_ids = yearly_sales_ids.filtered(
            lambda y: y.end_date == last_year_end_day.strftime("%Y-%m-%d"))
        if yearly_sales_ids:
            if yearly_sales_ids.sales_amount > amount:
                amount = yearly_sales_ids.sales_amount

        pricelist_policy = \
            self.property_product_pricelist.product_pricelist_policy_id
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
                        (sale_threshold_amount <= %s OR
                        sale_threshold_amount is NULL)
                    ORDER BY
                        sale_threshold_amount desc
                """, (available_pricelists, amount))
                new_pricelist = self._cr.dictfetchall()
                if new_pricelist:
                    if len(new_pricelist) > 1:
                        self.property_product_pricelist = new_pricelist[1]['id']
                    else:
                        self.property_product_pricelist = new_pricelist[0]['id']
        return True

    @api.multi
    def reset_partner_pricelist(self):
        for partner in self:
            last_year_start_day, last_year_end_day = self._get_year_dates(1)
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
                    line.name NOT LIKE %s AND
                    so.partner_id=%s AND
                    so.state = 'sale' AND
                    to_char(so.date_order, 'YYYY-MM-DD')::date >= %s AND
                    to_char(so.date_order, 'YYYY-MM-DD')::date <= %s
                GROUP BY
                    line.currency_id
                """, ('%Shipping Cost%',
                      partner.id,
                      last_year_start_day,
                      last_year_end_day)
            )
            sales_total = self._cr.dictfetchall()
            sales_total_amount = 0.0
            if sales_total:
                for data in sales_total:
                    if data['currency_id'] != partner.company_currency_id.id:
                        current_currency = self.env['res.currency']\
                            .sudo().browse(data['currency_id'])
                        exchange_amt = current_currency.compute(
                            data['line_total'],
                            partner.company_currency_id
                        )
                        sales_total_amount += exchange_amt
                    else:
                        sales_total_amount += data['line_total']

            yearly_sales_ids = partner.yearly_sales_history_ids
            yearly_sales_ids = yearly_sales_ids.filtered(
                lambda y: y.end_date == last_year_end_day.strftime("%Y-%m-%d")
            )

            if yearly_sales_ids:
                yearly_sales_ids[0].write({'sales_amount': sales_total_amount})
            else:
                vals = {
                    'partner_id': partner.id,
                    'start_date': last_year_start_day,
                    'end_date': last_year_end_day,
                    'sales_amount': sales_total_amount,
                }
                self.env['partner.yearly_sales'].sudo().create(vals)
            self._yearly_purchase_total()
            partner._update_current_pricelist()
        return True

    @api.multi
    def cron_reset_policy_pricelist(self):
        partners = self.env['res.partner']\
            .sudo().search([('customer','=', True)])
        partners.reset_partner_pricelist()
        return True


