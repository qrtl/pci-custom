# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def action_cancel(self):
        self.do_unreserve()
        res = super(StockPicking, self).action_cancel()
        return res

    @api.multi
    def write(self, vals):
        self.do_unreserve()
        res = super(StockPicking, self).write(vals)
        return res

