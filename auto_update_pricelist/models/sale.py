# -*- coding: utf-8 -*-

from openerp import models, api, fields
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.partner_id._update_currenct_pricelist()
        return res

    @api.multi
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        for order in self:
            default_pricelist = self.env['product.pricelist'].search([('is_default', '=', True)], limit=1)
            price_list = order.partner_id.property_product_pricelist.product_pricelist_policy_id.pricelist_ids
            for procelist_id in price_list:
                if procelist_id.is_default:
                    default_pricelist = procelist_id
            if default_pricelist:
                order.partner_id.property_product_pricelist = default_pricelist
            order.partner_id._update_currenct_pricelist()
        return res

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for order in self:
            order.partner_id._update_currenct_pricelist()
        return res