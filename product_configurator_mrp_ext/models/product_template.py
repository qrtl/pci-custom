# -*- coding: utf-8 -*-
# Copyright 2016-2017 Pledra
# Copyright 2017 Willdooit
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

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
