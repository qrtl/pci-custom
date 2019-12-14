# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_available_location = fields.Float(
        related="product_id.qty_available_location",
    )

    @api.multi
    def action_view_stock_moves(self):
        action = self.env.ref(
            'mrp_view_adj.act_product_reserving_stock_move_open'
        ).read()[0]
        action['context'] = {'search_default_ready': 1}
        action['domain'] = [('product_id', '=', self.product_id.id)]
        return action
