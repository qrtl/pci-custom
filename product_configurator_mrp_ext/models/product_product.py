# -*- coding: utf-8 -*-
# Copyright 2016-2017 Pledra
# Copyright 2017 Willdooit
# Copyright 2017-2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def configurator_default_bom_variant(self):
        self.ensure_one()
        result = self.product_tmpl_id.configurator_default_bom()
        result['product_id'] = self.id
        return result

    @api.multi
    def get_product_from_value_set(self):
        self.ensure_one()
        res = []
        categs = dict(self.env['product.template']._fields['part_categ'
            ].selection).keys()
        # return one mapped product per part category
        for categ in categs:
            value_sets = self.env['product.attribute.value.set'].search([
                ('product_tmpl_id', '=', self.product_tmpl_id.id),
                ('part_categ', '=', categ),
            ]).sorted(key=lambda r: len(r.value_ids), reverse=True)
            for value_set in value_sets:
                if set(value_set.value_ids).issubset(self.attribute_value_ids):
                    res.append({'product_id': value_set.product_id.id})
                    break
        return res

    @api.multi
    def configurator_create_bom(self):
        """Routine to create a bom,
        By default, this assumes that if there is a bom for the variant,
        then don't try and create another!
        """
        Mrp_bom = self.env['mrp.bom']
        for variant in self:
            if Mrp_bom.search([('product_id', '=', variant.id),
                               ('active', '=', True)]):
                continue
            values = variant.configurator_default_bom_variant()
            line_vals = values['bom_line_ids']
            # loop, don't use mapped, as the product may be mapped by multiple
            # attributes
            for attr_value in variant.attribute_value_ids:
                bom_line_vals = attr_value.bom_line_dictionary()
                if bom_line_vals:
                    line_vals.append((0, 0, bom_line_vals))

            bom_line_val_list = variant.get_product_from_value_set()
            if bom_line_val_list:
                for bom_line_vals in bom_line_val_list:
                    line_vals.append((0, 0, bom_line_vals))

            Mrp_bom.create(values)
