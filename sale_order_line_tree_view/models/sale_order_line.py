# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    expected_date = fields.Date(
        readonly=True,
        store=True,
        related='order_id.expected_date'
    )
    categ_id = fields.Many2one(
        readonly=True,
        store=True,
        related='product_id.categ_id'
    )
    to_be_delivered = fields.Boolean(
        readonly=True,
        store=True,
        default=False,
        string='To Be Delivered',
        compute='_compute_to_be_delivered'
    )

    @api.multi
    @api.depends('product_uom_qty', 'qty_delivered')
    def _compute_to_be_delivered(self):
        for order in self:
            if order.qty_delivered < order.product_uom_qty:
                order.to_be_delivered = True
            else:
                order.to_be_delivered = False
