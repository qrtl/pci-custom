# -*- coding: utf-8 -*-
# Copyright 2016-2017 Pledra
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
from ast import literal_eval


class ProductAttributeValueSet(models.Model):
    _name = 'product.attribute.value.set'


    config_step_line_id = fields.Many2one(
        comodel_name='product.config.step.line',
        string='Configuration Step Line',
    )
    config_step_id = fields.Many2one(
        comodel_name='product.config.step',
        related='config_step_line_id.config_step_id',
        readonly=True,
        # string='Configuration Step',
        # ondelete='cascade',
        # required=True
    )
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        related='config_step_line_id.product_tmpl_id',
        readonly=True,
        # string='Product Template',
        # ondelete='cascade',
        # required=True
    )
    # attribute_line_id = fields.Many2one(
    #     comodel_name='product.attribute.line',
    #     string='Attribute Line',
    #     ondelete='cascade',
    #     required=True
    # )
    # # TODO: Find a more elegant way to restrict the value_ids
    # attr_line_val_ids = fields.Many2many(
    #     comodel_name='product.attribute.value',
    #     related='attribute_line_id.value_ids'
    # )
    value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        # id1="cfg_line_id",
        # id2="attr_val_id",
        string="Values"
    )
    # domain_id = fields.Many2one(
    #     comodel_name='product.config.domain',
    #     required=True,
    #     string='Restrictions'
    # )
    # sequence = fields.Integer(string='Sequence', default=10)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
    )
