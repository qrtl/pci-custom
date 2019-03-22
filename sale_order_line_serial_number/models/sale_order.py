# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            # Pass the serial_number field from order line to the corresponding
            # manufacturing order
            for order_line in order.order_line:
                production_orders = []
                for procurement_order in order_line.procurement_ids:
                    for move_id in procurement_order.move_ids:
                        for original_move in move_id.move_orig_ids:
                            if original_move.production_id:
                                original_move.production_id.serial_number = \
                                    order_line.serial_number
                                production_orders.append(
                                    original_move.production_id)
                # Loop over the manufacturing orders to pass the
                # serial_number down to other related manufacturing orders
                # according to the "Consumed Materials" stock move
                while production_orders:
                    related_orders = production_orders
                    production_orders = []
                    for production_order in related_orders:
                        for move_raw_id in production_order.move_raw_ids:
                            for original_move in move_raw_id.move_orig_ids:
                                if original_move.production_id:
                                    original_move.production_id.serial_number = \
                                        order_line.serial_number
                                    production_orders.append(
                                        original_move.production_id)
        return res
