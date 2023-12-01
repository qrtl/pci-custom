# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.http import request
from odoo import models
from odoo.tools import float_is_zero
from odoo.addons.website_sale.models.product import Product

# Monkey Patching
# Overwrite the original _website_price in wabsite_sale
# i.e. https://github.com/odoo/odoo/blob/10.0/addons/website_sale/models
# /product.py#L196-L213


def _website_price(self):
    qty = self._context.get('quantity', 1.0)
    partner = self.env.user.partner_id
    current_website = self.env['website'].get_current_website()
    pricelist = current_website.get_current_pricelist()
    company_id = current_website.company_id

    # Added by QTL >>>
    # Check the request user
    # If the user is login-ed, apply the pricelist of the user
    if request.website and request.env.user != request.website.user_id and \
            request.uid != partner.id:
        pricelist = self.env["res.users"].browse(
            request.uid).property_product_pricelist
    # Added by QTL <<<

    context = dict(self._context, pricelist=pricelist.id, partner=partner)
    self2 = self.with_context(context) if self._context != context else self

    ret = (
        'total_excluded'
        if self.env.user.has_group('sale.group_show_price_subtotal')
        else 'total_included'
    )

    for p, p2 in zip(self, self2):
        taxes = partner.property_account_position_id.map_tax(
            p.taxes_id.sudo().filtered(lambda x: x.company_id == company_id)
        )
        p.website_price = taxes.compute_all(
            p2.price, pricelist.currency_id, quantity=qty, product=p2, partner=partner
        )[ret]
        price_without_pricelist = taxes.compute_all(
            p.list_price, pricelist.currency_id
        )[ret]
        p.website_price_difference = (
            False if float_is_zero(
                price_without_pricelist - p.website_price,
                precision_rounding=pricelist.currency_id.rounding
            ) else True
        )
        p.website_public_price = taxes.compute_all(
            p2.lst_price, quantity=qty, product=p2, partner=partner
        )[ret]


class ProductHookWebsitePrice(models.AbstractModel):
    _name = "product.hook.website.price"
    _description = "Provide hook point for _website_price method"

    def _register_hook(self):
        Product._website_price = _website_price
        return super(ProductHookWebsitePrice, self)._register_hook()
