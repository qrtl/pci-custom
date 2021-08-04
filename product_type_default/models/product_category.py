# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    product_type = fields.Selection(
        [
            ("consu", "Consumable"),
            ("service", "Service"),
            ("product", "Stockable Product"),
        ],
        string="Product Type",
    )
