# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_type = fields.Selection(related="product_id.type", store=True,)
    amt_rcvd_not_billed = fields.Monetary(
        compute="_compute_variance_amount", string="Received Not Billed", store=True,
    )
    amt_billed_not_rcvd = fields.Monetary(
        compute="_compute_variance_amount", string="Billed Not Received", store=True,
    )

    @api.depends("price_unit", "qty_received", "qty_invoiced")
    def _compute_variance_amount(self):
        for ln in self.filtered(lambda x: x.product_type in ["consu", "product"]):
            if ln.qty_received > ln.qty_invoiced:
                ln.amt_rcvd_not_billed = ln.price_unit * (
                    ln.qty_received - ln.qty_invoiced
                )
            elif ln.qty_received < ln.qty_invoiced:
                ln.amt_billed_not_rcvd = ln.price_unit * (
                    ln.qty_invoiced - ln.qty_received
                )
