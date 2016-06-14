# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _


class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    def onchange_serial(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, context=None, serial_id=False):

        res = super(sale_order_line, self).product_id_change(cr, uid, ids,
            pricelist=pricelist, product=product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag, context=context)
        if serial_id:
            lot_obj = self.pool.get('stock.production.lot').browse(cr, uid, serial_id, context)
            res['value'].update({'product_id': lot_obj.product_id.id})
            if product and product in [lot_obj.product_id.id]:
                res['value'].update({'price_unit': lot_obj.list_price})
        return res

#    def onchange_serial(self, cr, uid, ids, pricelist, product, qty=0,
#            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
#            lang=False, update_tax=True, date_order=False, packaging=False,
#            fiscal_position=False, flag=False, context=None, serial_id=False):
#
#        if serial_id:
#            lot_obj = self.pool.get('stock.production.lot').browse(cr, uid, serial_id, context)
#            return {'value': {'price_unit': lot_obj.list_price}}
#        else:
#            return super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist=pricelist,
#                product=product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos, name=name,
#                partner_id=partner_id, lang=lang, update_tax=update_tax, date_order=date_order,
#                packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, context=None, serial_id=False):

        res = super(sale_order_line, self).product_id_change(cr, uid, ids,
            pricelist=pricelist, product=product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag, context=context)
        if product:
            res['domain'].update({'serial_id': [('product_id','=',product)]})
        if serial_id:
            lot_obj = self.pool.get('stock.production.lot').browse(cr, uid, serial_id, context)
            if product and product not in [lot_obj.product_id.id]:
                res['value'].update({'serial_id': False})
            res['value'].update({'price_unit': lot_obj.list_price})
        return res


#    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
#            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
#            lang=False, update_tax=True, date_order=False, packaging=False,
#            fiscal_position=False, flag=False, context=None):
#
#        res = super(sale_order_line, self).product_id_change(cr, uid, ids,
#            pricelist=pricelist, product=product, qty=qty,
#            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
#            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging,
#            fiscal_position=fiscal_position, flag=flag, context=context)
#        if product:
#            product_obj = self.pool.get('product.product').browse(cr, uid, product, context)
#            res['value'].update({'track_outgoing': product_obj.track_outgoing})
#        return res

    _columns = {
        'serial_id': fields.many2one('stock.production.lot', 'Serial Number'),
        'track_outgoing': fields.boolean('Track Outgoing Lots',
            help="Forces to specify a Serial Number for all moves containing \
                this product and going to a Customer Location"),
    }

    _defaults = {
        'track_outgoing': False
    }

    def copy(self, cr, uid, id, default=None, context=None):
        default = {} if default is None else default.copy()
        default.update({
            'serial_id':False
        })
        return super(sale_order_line, self).copy(cr, uid, id, default=default, context=context)

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id = False, context=None):
        res = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line=line,
                                                                            account_id = account_id,
                                                                            context = context)
        res.update({'serial_id': line.serial_id.id})
        return res

class sale_order(osv.osv):
    _inherit = "sale.order"

    def _prepare_order_line_move(self, cr, uid, order, line, picking_id, date_planned, context=None):
        res = super(sale_order, self)._prepare_order_line_move(cr, uid, order, line,
                                                              picking_id=picking_id,
                                                              date_planned=date_planned,
                                                              context=context)
        res.update({'prodlot_id': line.serial_id.id})
        return res

    def action_wait(self, cr, uid, ids, context=None):
        context = context or {}
        for order in self.browse(cr, uid, ids, context):
            if order.order_line:
                serial_dict = {}
                for line in order.order_line:
                    if line.serial_id and line.product_id.product_tmpl_id.categ_id.enforce_qty_1 and line.product_uom_qty > 1.0:
                        raise osv.except_osv(_('Error!'), _('Quantity of SO line should be 1 for product %s (enforce quantity 1).')
                                                            % line.product_id.name)
                    if line.serial_id and line.product_id.product_tmpl_id.categ_id.enforce_qty_1 and line.serial_id.reserved_qty > 0.0:
                        raise osv.except_osv(_('Error!'),
                                             _('Sorry, product %s has been already reserved (enforce quantity 1).')
                                                            % line.product_id.name)
                    if line.serial_id and line.serial_id.id not in serial_dict:
                        serial_dict[line.serial_id.id] = 1
                    elif line.serial_id and line.serial_id.id in serial_dict:
                        serial_dict[line.serial_id.id] += 1
                for serial in serial_dict:
                    if serial_dict[serial] > 1:
                        serial_data = self.pool.get('stock.production.lot').browse(cr, uid, [serial], context)[0]
                        if serial_data.product_id.product_tmpl_id.categ_id.enforce_qty_1:
                            raise osv.except_osv(_('Error!'),
                                             _('Sorry, You can not have serial number same for multiple order lines - [%s]')
                                                            % serial_data.name)
        return super(sale_order, self).action_wait(cr, uid, ids, context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
