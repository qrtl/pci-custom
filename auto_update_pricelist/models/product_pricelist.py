# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models

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


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    sale_threshold_amount = fields.Float(
        string = 'Sale Threshold Amount',
        copy=False,
    )
    product_pricelist_policy_id = fields.Many2one(
        'product.pricelist.policy',
        string = 'Product Pricelist Policy',
        copy=False,
    )
    is_default = fields.Boolean(
        string="Default Pricelist?",
        copy=False,
    )
