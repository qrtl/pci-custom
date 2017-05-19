# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

"""to be deleted later """

# from openerp.osv import osv, fields
# import openerp.addons.decimal_precision as dp
#
# class account_invoice(osv.osv):
#     _inherit = "account.invoice"
#
#     def action_move_create(self, cr, uid, ids, context=None):
#         res = super(account_invoice, self).action_move_create(cr, uid, ids, context)
#         invoice_line_obj = self.pool.get('account.invoice.line')
#         for inv in self.browse(cr, uid, ids, context):
#             for line in inv.invoice_line:
#                 if line.serial_id:
#                     invoice_line_obj.write(cr, uid, [line.id], {'serial_standard_price': line.serial_id.standard_price}, context=context)
#         return res
