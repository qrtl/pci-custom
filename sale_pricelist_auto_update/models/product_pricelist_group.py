# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductPricelistGroup(models.Model):
    _name = "product.pricelist.group"

    name = fields.Char(required=True,)
    pricelist_ids = fields.One2many(
        comodel_name="product.pricelist",
        inverse_name="pricelist_group_id",
        string="Pricelists",
    )
