# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductPricelistGroup(models.Model):
    _name = "product.pricelist.group"

    name = fields.Char(required=True,)
    pricelist_ids = fields.One2many(
        comodel_name="product.pricelist",
        inverse_name="pricelist_group_id",
        string="Pricelists",
    )
