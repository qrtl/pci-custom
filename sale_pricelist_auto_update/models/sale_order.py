# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_order_ctx = fields.Date(
        compute="_get_date_order_ctx", store=True, string="Order Date (No Time)",
    )

    @api.multi
    @api.depends("date_order")
    def _get_date_order_ctx(self):
        # set date_order_ctx based on user's timezone
        for order in self:
            datetime_order_ctx = fields.Datetime.context_timestamp(
                order, fields.Datetime.from_string(order.date_order)
            )
            order.date_order_ctx = fields.Date.context_today(order, datetime_order_ctx)

    @api.multi
    def _get_date_range(self):
        self.ensure_one()
        return self.env["date.range"].search(
            [
                ("active", "=", True),
                ("date_start", "<=", self.date_order_ctx),
                ("date_end", ">=", self.date_order_ctx),
                ("is_fiscal_year", "=", True),
                ("company_id", "=", self.company_id.id),
            ],
            limit=1,
        )

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for order in self:
            if (
                vals.get("state", False) in ("sale", "done", "cancel")
                or "order_line" in vals
                and order.state == "sale"
            ):
                date_range = order._get_date_range()
                if date_range:
                    self.env["res.partner"].reset_partner_pricelist(
                        date_range, order.partner_id
                    )
        return res
