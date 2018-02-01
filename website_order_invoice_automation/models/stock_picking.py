# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        if 'date_done' in vals:
            for pick in self:
                pick._check_sale_order()
        return res

    def _check_sale_order(self):
        if self.picking_type_id.code == "outgoing" and self.sale_id and \
                self.sale_id.team_id and self.sale_id.team_id.auto_invoice:
            for order_line in self.sale_id.order_line:
                if order_line.qty_to_invoice > 0:
                    self.sale_id._generate_and_validate_invoice()
                    return
