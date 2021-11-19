# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        if vals.get("picking_type_id"):
            for pick in self:
                pick.name = pick.picking_type_id.sequence_id.next_by_id()
        return res
