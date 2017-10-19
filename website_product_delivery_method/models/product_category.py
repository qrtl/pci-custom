# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    free_delivery = fields.Boolean(
        string="Free Delivery Fee",
        copy=False,
    )