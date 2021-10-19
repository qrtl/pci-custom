# -*- coding: utf-8 -*-
# Copyright 2016-2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    # originally "@api.onchange('product_uom', 'product_uom_qty')" - remove
    # product_uom_qty from the trigger
    @api.onchange("product_uom")
    def _onchange_quantity(self):
        return super(PurchaseOrderLine, self)._onchange_quantity()
