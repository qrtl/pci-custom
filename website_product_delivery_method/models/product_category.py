# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    free_fix_delivery = fields.Boolean(
        string="Free/Fixed-price Delivery",
        copy=False,
        oldname="free_delivery",
    )
