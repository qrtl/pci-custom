# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class stock_inventory(osv.osv):
    _inherit = "stock.inventory"

    def action_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for inv in self.browse(cr, uid, ids, context=context):
            serial_dict = {}
            for move in inv.inventory_line_id:
                if move.prod_lot_id and move.prod_lot_id.id not in serial_dict:
                    serial_dict[move.prod_lot_id.id] = 1
                elif move.prod_lot_id and move.prod_lot_id.id in serial_dict:
                    serial_dict[move.prod_lot_id.id] += 1
            for serial in serial_dict:
                if serial_dict[serial] > 1:
                    serial_data = self.pool.get('stock.production.lot').browse(cr, uid, [serial], context)[0]
                    if serial_data.product_id.product_tmpl_id.categ_id.enforce_qty_1:
                        raise osv.except_osv(_('Error!'),
                                         _('Sorry, You can not have serial number same for multiple inventory lines - [%s]')
                                                        % serial_data.name)
        return super(stock_inventory, self).action_confirm(cr, uid, ids, context=context)
