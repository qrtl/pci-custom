# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductSpecialTag(models.Model):
    _description = 'Special Tags'
    _name = 'product.special.tag'

    name = fields.Char(
        string='Tag Name',
        required=True,
        translate=True,
    )
    color = fields.Integer(
        string='Color Index'
    )
    active = fields.Boolean(
        default=True,
    )
    product_tmpl_ids = fields.Many2many(
        'product.template',
        column1='special_tag_id',
        column2='product_tmpl_id',
        string='Products'
    )
