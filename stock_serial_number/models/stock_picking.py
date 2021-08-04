# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _


class stock_picking(osv.osv):
    _inherit = "stock.picking"

    def action_done(self, cr, uid, ids, context=None):
        pickings = self.browse(cr, uid, ids, context=context)
        for picking in pickings:
            serial_dict = {}
            for move in picking.move_lines:
                if move.prodlot_id and move.prodlot_id.id not in serial_dict:
                    serial_dict[move.prodlot_id.id] = 1
                elif move.prodlot_id and move.prodlot_id.id in serial_dict:
                    serial_dict[move.prodlot_id.id] += 1
            for serial in serial_dict:
                if serial_dict[serial] > 1:
                    serial_data = self.pool.get('stock.production.lot').browse(cr, uid, [serial], context)[0]
                    if serial_data.product_id.product_tmpl_id.categ_id.enforce_qty_1:
                        raise osv.except_osv(_('Error!'),
                                         _('Sorry, You can not have serial number same for multiple move lines - [%s]')
                                                        % serial_data.name)
        return super(stock_picking, self).action_done(cr, uid, ids, context=context)
