# -*- coding: utf-8 -*-
# Copyright 2016-2017 Pledra
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, _


class ProductConfigStepLine(models.Model):
    _inherit = 'product.config.step.line'


    attribute_value_set_ids = fields.Many2many(
        comodel_name='product.attribute.value.set',
        string='Attribute Value Sets',
    )
