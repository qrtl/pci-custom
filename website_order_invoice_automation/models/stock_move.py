# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_done(self):
        result = super(StockMove, self).action_done()
        for stock_move in self:
            stock_picking = stock_move.picking_id
            if stock_picking.picking_type_id.code == "outgoing" and \
                    stock_picking.sale_id and stock_picking.sale_id.team_id and \
                    stock_picking.sale_id.team_id.auto_invoice and \
                    stock_picking.sale_id._is_invoiceable():
                stock_picking.sale_id._generate_and_validate_invoice()
        return result
