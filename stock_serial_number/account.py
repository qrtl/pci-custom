# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"

    _columns = {
        'serial_id': fields.many2one('stock.production.lot', 'Serial Number'),
        'standard_price': fields.related('serial_id', 'standard_price', string='Cost Price', digits_compute=dp.get_precision('Product Price'), groups="base.group_user", type='float'),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        default = {} if default is None else default.copy()
        default.update({
            'serial_id':False
        })
        return super(account_invoice_line, self).copy(cr, uid, id, default=default, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
