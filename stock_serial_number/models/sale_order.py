# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # def _prepare_order_line_move(self, cr, uid, order, line, picking_id, date_planned, context=None):
    #     res = super(sale_order, self)._prepare_order_line_move(cr, uid, order, line,
    #                                                           picking_id=picking_id,
    #                                                           date_planned=date_planned,
    #                                                           context=context)
    #     res.update({'prodlot_id': line.serial_id.id})
    #     return res

    # def action_wait(self, cr, uid, ids, context=None):
    #     context = context or {}
    #     for order in self.browse(cr, uid, ids, context):
    #         if order.order_line:
    #             serial_dict = {}
    #             for line in order.order_line:
    #                 if line.serial_id and line.product_id.product_tmpl_id.categ_id.enforce_qty_1 and line.product_uom_qty > 1.0:
    #                     raise osv.except_osv(_('Error!'), _('Quantity of SO line should be 1 for product %s (enforce quantity 1).')
    #                                                         % line.product_id.name)
    #                 if line.serial_id and line.product_id.product_tmpl_id.categ_id.enforce_qty_1 and line.serial_id.reserved_qty > 0.0:
    #                     raise osv.except_osv(_('Error!'),
    #                                          _('Sorry, product %s has been already reserved (enforce quantity 1).')
    #                                                         % line.product_id.name)
    #                 if line.serial_id and line.serial_id.id not in serial_dict:
    #                     serial_dict[line.serial_id.id] = 1
    #                 elif line.serial_id and line.serial_id.id in serial_dict:
    #                     serial_dict[line.serial_id.id] += 1
    #             for serial in serial_dict:
    #                 if serial_dict[serial] > 1:
    #                     serial_data = self.pool.get('stock.production.lot').browse(cr, uid, [serial], context)[0]
    #                     if serial_data.product_id.product_tmpl_id.categ_id.enforce_qty_1:
    #                         raise osv.except_osv(_('Error!'),
    #                                          _('Sorry, You can not have serial number same for multiple order lines - [%s]')
    #                                                         % serial_data.name)
    #     return super(sale_order, self).action_wait(cr, uid, ids, context)

    @api.multi
    def action_confirm(self):
        for order in self:
            if order.order_line:
                lot_ids = []
                for l in order.order_line.filtered(
                        lambda l: l.lot_id != False and
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

    # @api.multi
    # def action_confirm(self):
    #     for order in self:
    #         order.state = 'sale'
    #         order.confirmation_date = fields.Datetime.now()
    #         if self.env.context.get('send_email'):
    #             self.force_quotation_send()
    #         order.order_line._action_procurement_create()
    #     if self.env['ir.values'].get_default('sale.config.settings',
    #                                          'auto_done_setting'):
    #         self.action_done()
    #     return True
