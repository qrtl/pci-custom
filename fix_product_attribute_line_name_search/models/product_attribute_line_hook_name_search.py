# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.addons.product.models.product_attribute import ProductAttributeLine
from odoo.osv import expression

"""
Odoo's original method completely overrides `args` which disables whatever
domain passed to this method, and therefore is not desiable.
We will fix it by extending args instead of overriding it.
Ref: https://github.com/odoo/odoo/pull/26133
"""


@api.model
def name_search(self, name="", args=None, operator="ilike", limit=100):
    # TDE FIXME: currently overriding the domain; however as it includes a
    # search on a m2o and one on a m2m, probably this will quickly become
    # difficult to compute - check if performance optimization is required
    if name and operator in ("=", "ilike", "=ilike", "like", "=like"):
        # args = ['|', ('attribute_id', operator, name), ('value_ids', operator, name)]  # QTL del
        args = args or []  # QTL add
        domain = [
            "|",
            ("attribute_id", operator, name),
            ("value_ids", operator, name),
        ]  # QTL add
        return self.search(
            expression.AND([domain, args]), limit=limit
        ).name_get()  # QTL add
    return super(ProductAttributeLine, self).name_search(
        name=name, args=args, operator=operator, limit=limit
    )


class ProductAttributeLineHookNameSearch(models.AbstractModel):
    _name = "product.attribute.line.hook.name.search"
    _description = "Provide hook point for name_search method"

    def _register_hook(self):
        ProductAttributeLine.name_search = name_search
        return super(ProductAttributeLineHookNameSearch, self)._register_hook()
