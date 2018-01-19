# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # set default to zero to avoid having 1.0 price for non-sellable products
    # which could affect price proposal using product configurator
    list_price = fields.Float(default=0.0)
