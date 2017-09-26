# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_received_adj = fields.Float(
        string='Received Qty',
        compute='_compute_qty_received_adj',
        digits=dp.get_precision('Product Unit of Measure'),
        copy=False,
        store=True,
        default=0.0
    )

    @api.depends('qty_received', 'qty_returned')
    def _compute_qty_received_adj(self):
        for line in self:
            line.qty_received_adj =  line.qty_received - line.qty_returned
