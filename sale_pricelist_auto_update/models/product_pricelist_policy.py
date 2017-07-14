# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProductPricelistPolicy(models.Model):
    _name = "product.pricelist.policy"
    _rec_name = 'tag'

    tag = fields.Char(
        string = "Tag",
        help = 'Tag for the set of pricelists',
        required=True,
    )
    pricelist_ids = fields.Many2many(
        'product.pricelist',
        string = 'Pricelists',
        required=True,
        )
