# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class account_invoice(osv.osv):
    _inherit = "account.invoice"

    def action_move_create(self, cr, uid, ids, context=None):
        res = super(account_invoice, self).action_move_create(cr, uid, ids, context)
        invoice_line_obj = self.pool.get('account.invoice.line')
        for inv in self.browse(cr, uid, ids, context):
            for line in inv.invoice_line:
                if line.serial_id:
                    invoice_line_obj.write(cr, uid, [line.id], {'serial_standard_price': line.serial_id.standard_price}, context=context)
        return res

class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"

    _columns = {
        'serial_id': fields.many2one('stock.production.lot', 'Serial Number'),
        'serial_standard_price': fields.float('Cost Price', digits_compute=dp.get_precision('Product Price'), groups="base.group_user", readonly=True),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        default = {} if default is None else default.copy()
        default.update({
            'serial_id':False,
            'serial_standard_price': 0.0,
        })
        return super(account_invoice_line, self).copy(cr, uid, id, default=default, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
