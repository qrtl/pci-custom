# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange('categ_id')
    def onchange_categ_id(self):
        if self.categ_id:
            self.type = self.categ_id.product_type
