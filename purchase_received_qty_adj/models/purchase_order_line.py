# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_received_net = fields.Float(
        string='Received Qty (Net)',
        compute='_compute_qty_received_adj',
        digits=dp.get_precision('Product Unit of Measure'),
        copy=False,
        store=True,
        default=0.0,
        help='This field shows the net received qty (Received Qty minus '
             'Returned Qty'
    )

    @api.depends('qty_received', 'qty_returned')
    def _compute_qty_received_adj(self):
        for line in self:
            line.qty_received_net = line.qty_received - line.qty_returned
