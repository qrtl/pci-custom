# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


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
