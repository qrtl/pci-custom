# -*- coding: utf-8 -*-
# Copyright 2017-2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_delivery_methods(self):

        available_carriers = super(SaleOrder, self)._get_delivery_methods()
        if available_carriers:
            partner_id = self.partner_id

            # if customer group set on partner then filter delivery method
            # with matching of partner customer group
            if partner_id.customer_group:
                available_carriers = available_carriers.filtered(
                    lambda d: (not d.customer_group) or d.customer_group ==
                                  partner_id.customer_group)
            # if all order lines are belongs from Free/Fixed Price product
            # category, set the cheapest delivery as the delivery method.
            non_delivery_line = self.order_line.filtered(lambda i : not
            i.is_delivery)
            if all(i.product_id.categ_id.free_fix_delivery for i in
                   non_delivery_line):
                available_carriers = available_carriers.filtered(
                    lambda i: i.delivery_type == "fixed").sorted(
                        lambda x: x.fixed_price)[0]
            else:
                available_carriers = available_carriers.filtered(
                    lambda i: not(i.delivery_type == "fixed"))
        return available_carriers
