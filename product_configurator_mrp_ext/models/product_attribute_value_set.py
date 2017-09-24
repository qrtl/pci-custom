# -*- coding: utf-8 -*-
# Copyright 2016-2017 Pledra
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProductAttributeValueSet(models.Model):
    _name = 'product.attribute.value.set'
    _order = 'sequence'


    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        ondelete='cascade',
    )
    value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        string="Values",
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
        help="This product will be included as a BOM component for the given "
             "set of attribute values.",
    )
