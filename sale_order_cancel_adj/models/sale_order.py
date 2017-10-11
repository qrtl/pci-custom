# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_cancel(self):
        self.mapped('picking_ids').action_cancel()
        return super(SaleOrder, self).action_cancel()
