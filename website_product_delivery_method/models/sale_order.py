# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
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
            # if all order lines are belongs from free delivery product
            # category then return only free delivery methods
            non_delivery_line = self.order_line.filtered(lambda i : not
            i.is_delivery)
            if all(i.product_id.categ_id.free_delivery for i in
                   non_delivery_line):
                available_carriers = available_carriers.filtered(
                    lambda i:i.fixed_price == 0.0)
            else:
                available_carriers = available_carriers.filtered(
                    lambda i: not(i.delivery_type == "fixed" and
                                  i.fixed_price == 0.0))
        return available_carriers
