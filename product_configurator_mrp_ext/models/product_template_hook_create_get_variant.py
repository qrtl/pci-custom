# -*- coding: utf-8 -*-
# Copyright 2016-2017 Pledra
# Copyright 2017 Willdooit
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api
from odoo.exceptions import ValidationError
from odoo.addons.product_configurator_mrp.models.product import ProductTemplate


@api.multi
def create_get_variant(self, value_ids, custom_values=None):
    if custom_values is None:
        custom_values = {}
    valid = self.validate_configuration(value_ids, custom_values)
    if not valid:
        raise ValidationError(_('Invalid Configuration'))

    duplicates = self.search_variant(value_ids,
                                     custom_values=custom_values)
    if custom_values:
        value_custom_ids = self.encode_custom_values(custom_values)
        if any('attachment_ids' in cv[2] for cv in value_custom_ids):
            duplicates = False
    if duplicates:
        duplicates[0].configurator_create_bom()
        return duplicates[0]
    vals = self.get_variant_vals(value_ids, custom_values)
    variant = self.env['product.product'].create(vals)
    variant.configurator_create_bom()
    return variant


class ProductTemplateHookCreateGetVariant(models.AbstractModel):
    _name = "product.template.hook.crate.get.variant"
    _description = "Provide hook point for create_get_variant method"

    def _register_hook(self):
        ProductTemplate.create_get_variant = create_get_variant
        return super(ProductTemplateHookCreateGetVariant, self).\
            _register_hook()
