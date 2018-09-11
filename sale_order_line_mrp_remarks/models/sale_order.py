# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            manufacturing_orders = order.production_ids
            # Sort the orders according to the ids, therefore the root order
            # will be come back the leaf orders
            for manufacturing_order in sorted(manufacturing_orders,
                                              key=lambda x: x.id):
                order_line = order.order_line.filtered(
                    lambda t: t.product_id.product_tmpl_id ==
                              manufacturing_order.product_id.product_tmpl_id)
                # Set remarks to the root order
                if order_line:
                    manufacturing_order.remarks = order_line[0].remarks
                # Find the related procurement orders to pass the remarks
                # field to one level below of the manufacturing order
                related_procurement_orders = self.env[
                    'procurement.order'].search([
                    ('origin', 'like', '%%%s%%' % manufacturing_order.name)
                ])
                for procurement_order in related_procurement_orders:
                    # Set remarks to the leaf order
                    if procurement_order.production_id:
                        procurement_order.production_id.remarks = \
                            manufacturing_order.remarks
        return res
