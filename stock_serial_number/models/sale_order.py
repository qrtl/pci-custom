# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.multi
    def action_confirm(self):
        for order in self:
            if order.order_line:
                lot_ids = []
                for l in order.order_line.filtered(
                        lambda l: l.lot_id and
                                        l.product_id.tracking == 'serial'):
                    if l.product_uom_qty > 1.0:
                        raise UserError(_('Quantity of SO line should be 1 '
                                          'for product %s.')
                                        % l.product_id.name)
                    if l.lot_id.reserved_qty > 0.0:
                        raise UserError(_('Serial %s has already been '
                                          'reserved for another order.')
                                        % l.lot_id.name)
                    if l.lot_id.id not in lot_ids:
                        lot_ids.append(l.lot_id.id)
                    else:
                        raise UserError(_('You cannot use the same serial in '
                                          'multiple lines - [%s]')
                                        % l.lot_id.name)
        return super(SaleOrder, self).action_confirm()
