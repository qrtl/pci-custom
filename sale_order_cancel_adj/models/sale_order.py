# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Related Github PR: https://github.com/odoo/odoo/pull/18121
    @api.multi
    def action_cancel(self):
        self.mapped("picking_ids").action_cancel()
        return super(SaleOrder, self).action_cancel()
