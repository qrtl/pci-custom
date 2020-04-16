# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_done(self):
        result = super(StockMove, self).action_done()
        picks = self.mapped('picking_id')
        for pick in picks:
            if pick.picking_type_id.code == "outgoing" and \
                    pick.sale_id and pick.sale_id.team_id and \
                    pick.sale_id.team_id.auto_invoice and \
                    pick.sale_id._is_invoiceable():
                pick.sale_id._generate_and_validate_invoice()
        return result
