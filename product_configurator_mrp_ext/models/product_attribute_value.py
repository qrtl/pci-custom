# -*- coding: utf-8 -*-
# Copyright 2016-2017 Pledra
# Copyright 2017 Willdooit
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.multi
    def bom_line_dictionary(self):
        self.ensure_one()
        result = {}
        if self.product_id:
            result.update(
                {'product_id': self.product_id.id}
            )
        return result
