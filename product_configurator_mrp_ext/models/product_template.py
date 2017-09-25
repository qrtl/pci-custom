# -*- coding: utf-8 -*-
# Copyright 2016-2017 Pledra
# Copyright 2017 Willdooit
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"


    attribute_value_set_ids = fields.One2many(
        comodel_name='product.attribute.value.set',
        inverse_name='product_tmpl_id',
        string='Attribute Value Sets',
    )

    @api.multi
    def configurator_default_bom(self):
        """
        :returns default dictionary bom to use as a default bom to include
        in every configuration

        Handy for overwriting.
        """
        return {
            'product_tmpl_id': self.id,
            'bom_line_ids': [],
        }
