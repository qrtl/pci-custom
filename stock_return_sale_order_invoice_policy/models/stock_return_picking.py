# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    @api.multi
    def _create_returns(self):
        new_picking_id, pick_type_id = super(
            StockReturnPicking, self)._create_returns()
        refund_flag = False
        for move in self.product_return_moves:
            if move.to_refund_so:
                refund_flag = True
        if refund_flag:
            return_picking = self.env['stock.picking'].browse(new_picking_id)
            if return_picking.group_id:
                sale_order = self.env['sale.order'].search([
                    ('procurement_group_id', '=', return_picking.group_id.id)
                ])
                if sale_order:
                    sale_order.update_invoice_policy = True
        return new_picking_id, pick_type_id
