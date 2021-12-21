# -*- coding: utf-8 -*-
# Copyright 2017-2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = "res.partner"

    yearly_sales_history_ids = fields.One2many(
        "partner.yearly_sales", "partner_id", string="Yearly Sales", copy=False,
    )
    company_currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id",
        store=True,
        readonly=True,
        string="Company Currency",
    )
    fix_pricelist = fields.Boolean(
        store=True,
        default=False,
        string="Fixed Pricelist",
        help="""If selected, the partner will be excluded
             from pricelist auto-update.""",
    )

    @api.multi
    def _update_current_pricelist(self):
        self.ensure_one()
        today = fields.Date.context_today(self)
        last_year = fields.Date.to_string(
            fields.Date.from_string(today) + relativedelta(years=-1)
        )
        hist_recs = self.commercial_partner_id.yearly_sales_history_ids.filtered(
            lambda x: (x.start_date <= today and x.end_date >= today)
            or (x.start_date <= last_year and x.end_date >= last_year)
        )
        amount = (
            hist_recs.sorted(key=lambda r: r.amt_total)[-1].amt_total
            if hist_recs
            else 0
        )
        group = self.property_product_pricelist.pricelist_group_id
        if group and not self.fix_pricelist:
            new_pricelist = self.env["product.pricelist"].search(
                [
                    ("pricelist_group_id", "=", group.id),
                    ("active", "=", True),
                    ("sale_threshold_amt", "<=", amount),
                ],
                order="sale_threshold_amt desc",
                limit=1,
            )
            if new_pricelist:
                if self.property_product_pricelist != new_pricelist:
                    self.property_product_pricelist = new_pricelist
            else:
                raise UserError(
                    _("Cannot find a pricelist that matches the conditions.")
                )
        return True

    # Considering a company could have more than one contact has its own
    # sales orders. This method will return all partners that are having the
    # same commercial_partner_id with the input partner_id in order to
    # aggregate the sales amounts.
    def _get_related_partners(self, partner=False):
        domain = [("customer", "=", True), ("active", "=", True)]
        if partner:
            domain = expression.AND(
                [
                    domain,
                    [("commercial_partner_id", "=", partner.commercial_partner_id.id)],
                ]
            )
        return self.env["res.partner"].sudo().search(domain)

    @api.multi
    def _update_partner_purchase_data(self, amount, date_start, date_end):
        self.ensure_one()
        # assumption: only one record should match if any
        history_recs = self.yearly_sales_history_ids.filtered(
            lambda x: x.end_date == date_end
        )
        if history_recs:
            if history_recs[0].amt_computed != amount:
                history_recs[0].write({"amt_computed": amount})
        else:
            vals = {
                "partner_id": self.id,
                "start_date": date_start,
                "end_date": date_end,
                "amt_computed": amount,
            }
            self.env["partner.yearly_sales"].sudo().create(vals)

    @api.multi
    def reset_partner_pricelist(self, date_range, partner=False):
        date_start = date_range.date_start
        date_end = date_range.date_end
        partners = self._get_related_partners(partner)
        shipping_products = self.env["product.product"].search(
            [("is_shipping_cost", "=", True)]
        )
        if shipping_products:
            params = (
                tuple(shipping_products.ids),
                tuple(partners.ids),
                date_start,
                date_end,
            )
        else:
            params = (tuple(partners.ids), date_start, date_end)
        sql = """
            SELECT
                p.commercial_partner_id AS partner_id,
                SUM(sol.base_amt) AS amount
            FROM
                sale_order_line sol
            JOIN
                sale_order so ON sol.order_id = so.id
            JOIN
                res_partner p ON so.partner_id = p.id
            WHERE
                sol.is_delivery IS FALSE AND
        """
        if shipping_products:
            sql += """
                sol.product_id NOT IN %s AND
            """
        sql += """
                so.partner_id in %s AND
                so.state in ('sale', 'done') AND
                so.date_order_ctx >= %s AND
                so.date_order_ctx <= %s
            GROUP BY
                p.commercial_partner_id
            """
        self._cr.execute(sql, params)
        sales_data = self._cr.dictfetchall()
        if not sales_data and partner and partner.commercial_partner_id:
            sales_data = [{"partner_id": partner.commercial_partner_id.id, "amount": 0}]
        for sales_dict in sales_data:
            partner = self.env["res.partner"].browse(sales_dict["partner_id"])
            if partner:
                partner._update_partner_purchase_data(
                    sales_dict["amount"], date_start, date_end
                )
        for partner in partners:
            partner._update_current_pricelist()
        return True
