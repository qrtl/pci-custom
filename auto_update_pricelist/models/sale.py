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
            order.partner_id._update_currenct_pricelist()
        return res

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for order in self:
            order.partner_id._update_currenct_pricelist()
        return res