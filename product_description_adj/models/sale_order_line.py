# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        # override name field not to include the the followings:
        # - product.description_sale
        # - product.default_code
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id:
            name = self.product_id.with_context(
                display_default_code=False).name_get()[0][1]
            self.update({'name': name})
        return res
