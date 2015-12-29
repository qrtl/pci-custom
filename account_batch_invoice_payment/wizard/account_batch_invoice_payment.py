# -*- coding: utf-8 -*-
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Rooms For (Hong Kong) Limited T/A OSCG
#    <https://www.odoo-asia.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class invoice_payment_wizard(osv.osv_memory):
    _name = 'invoice.payment.wizard'
    _columns = {
        'shop_id': fields.many2one('sale.shop', 'Shop',
            help='Draft customer invoices related to this shop will be filtered for validation and payment.'),
        'next_shipment_date': fields.date('Next Shipment Date',
            help='Draft customer invoices related to orders expected to be shipped on or before this date will be validated and paid.'),
    }

    def onchange_shop_id(self, cr, uid, ids, shop_id=False, context=None):
        res = {}
        if shop_id:
            next_shipment_date = self.pool.get('sale.shop').get_next_shipment_date(cr, uid, shop_id, False, context)
            res['value'] = {'next_shipment_date': next_shipment_date}
        return res


    def _get_invoice_ids(self, cr, uid, shop_id, next_shipment_date, context=None):
        inv_obj = self.pool.get('account.invoice')
        pick_obj = self.pool.get('stock.picking')
        draft_inv_ids = inv_obj.search(cr, uid,
            [('state','=','draft'),
             ('type','=','out_invoice')])
        res = []
        # filter invoices with shop_id and next_shipment_date
        for inv in inv_obj.browse(cr, uid, draft_inv_ids):
#             if not invoice.origin.startswith('SO'):
            sale_id = self.pool.get('sale.order').search(cr, uid, [('name', '=', inv.origin), ('order_policy', '=', 'manual')], context=context)
            if sale_id:
                pick_ids = pick_obj.search(cr, uid, [('sale_id', '=', sale_id[0])], context=context)
#             invoice_data.append({'invoice_id': invoice.id, 'sale_id': sale_id, 'do_id': pick_id})
                if pick_ids:
                    min_pick_date = datetime(9999, 12, 31).date()
                    for pick in pick_obj.browse(cr, uid, pick_ids, context=context):
                        pick_date = datetime.strptime(pick.min_date, '%Y-%m-%d %H:%M:%S').date()
                        if pick_date < min_pick_date:
                            min_pick_date = pick_date
                    if min_pick_date <= datetime.strptime(next_shipment_date, '%Y-%m-%d').date():
                        res.append(inv.id)
        return res


    def _get_journal(self, cr, uid, context=None):
        journal_obj = self.pool.get('account.journal')
        journal_id = journal_obj.search(cr, uid, [('default_payment_method','=',True)], context=context)
        if journal_id:
            return journal_obj.browse(cr, uid, journal_id, context=context)[0]
        else:
            return False

    
    def _batch_validate_invoice(self, cr, uid, inv_ids, context=None):
        inv_obj = self.pool.get('account.invoice')
        inv_validated = []
        for inv_id in inv_ids:
            try:  # validate invoice using workflow
                netsvc.LocalService('workflow').trg_validate(uid, 'account.invoice', inv_id, 'invoice_open', cr)
                inv_validated.append(inv_id)
            except:
                _logger.info('Invoice Fail: This invoice is failed during auto confirm wizard %s' %(inv_id))
        return inv_validated
    
    
    def _batch_pay_invoice(self, cr, uid, inv_validated, context=None):
        inv_obj = self.pool.get('account.invoice')
        voucher_obj = self.pool.get('account.voucher')
        for inv in inv_obj.browse(cr, uid, inv_validated):
            if inv.partner_id.is_company:
                partner_id = invoice.partner_id.id
            elif not inv.partner_id.is_company and inv.partner_id.parent_id:
                partner_id = inv.partner_id.parent_id.id
            else:
                partner_id = inv.partner_id.id
            
            # support multi currency
            curr_obj = self.pool.get('res.currency')
            journal = self._get_journal(cr, uid, context=context)
            if journal and journal.currency and journal.currency.id != inv.currency_id.id:
                curr_id_voucher = journal.currency.id
                voucher_amount = curr_obj.compute(cr, uid, inv.currency_id.id,
                        journal.currency.id,
                        inv.amount_total, round=False, context=context)
            elif not journal.currency and inv.currency_id.id != inv.company_id.currency_id.id:
                curr_id_voucher = inv.company_id.currency_id.id
                voucher_amount = curr_obj.compute(cr, uid, inv.currency_id.id, 
                        inv.company_id.currency_id.id,
                        inv.amount_total, round=False, context=context)
            else:
                curr_id_voucher = inv.currency_id.id
                voucher_amount = inv.amount_total
            
            today = fields.date.context_today(self, cr, uid, context=context)
            result = voucher_obj.onchange_partner_id(cr, uid, [], partner_id,
                        journal.id, invoice.amount_total,
                        invoice.currency_id.id, ttype='receipt',
                        date=today, context=context)
            journal_data = voucher_obj.onchange_journal_voucher(cr, uid, [],
                        line_ids=False,
                        tax_id=False,
                        price=inv.amount_total,
                        partner_id=inv.partner_id.id,
                        journal_id=journal.id,
                        ttype='receipt',
                        company_id=inv.company_id.id,
                        context=context)
            
            line_cr_list = []
            for line_dict in result['value']['line_cr_ids']:
                move_line = self.pool.get('account.move.line').browse(cr, uid,
                        line_dict['move_line_id'], context)
                if inv.move_id.id == move_line.move_id.id:
                    line_dict['amount'] = voucher_amount
                    line_cr_list.append((0, 0, line_dict))
            
            voucher_res = {
                    'type': 'receipt',
                    'reference': journal.name,
                    'name': inv.number,
                    'partner_id': partner_id,
                    'journal_id': journal.id,
                    'account_id': journal_data['value']['account_id'],
                    'company_id': inv.company_id.id,
                    'currency_id': curr_id_voucher,
                    'date': today,
                    'amount': voucher_amount,
                    'line_cr_ids' : line_cr_list,
                    'line_dr_ids' : False,
                    'state': 'draft',
                    'payment_rate': journal_data['value']['payment_rate'],
                    'payment_rate_currency_id': journal_data['value']['payment_rate_currency_id'],
                    }
            # create voucher for current invoice
            voucher_id = voucher_obj.create(cr, uid, voucher_res, context=context)
            try:  # post created voucher
                netsvc.LocalService('workflow').trg_validate(uid, 'account.voucher', voucher_id, 'proforma_voucher', cr)
            except:
                _logger.info('Voucher Validation Fail: This voucher is failed during auto create payment %s' %(voucher_id))
#         return inv_confirmed


#     def auto_invoice_payment(self, cr, uid, context=None):
#         if not context:
#             context = {}
#         shop_obj = self.pool.get('sale.shop')
# #         journal_obj = self.pool.get('account.journal')
#         inv_obj = self.pool.get('account.invoice')
#         pick_obj = self.pool.get('stock.picking')
#         voucher_obj = self.pool.get('account.voucher')
#         
#         wf_service = netsvc.LocalService('workflow')
#         user = self.pool.get('res.users').browse(cr, uid, uid)
#         company_id = user.company_id.id
#         
#         # find the shop of current company
#         shop_id = shop_obj.search(cr, uid, [('company_id', '=', company_id)], context=context)[0]
#         shop = shop_obj.browse(cr, uid, shop_id, context=context)
#         shipment_day = shop.shipment_day
#         
#         today = datetime.date.today()
#         # find the date of next shipment day defined on sale shop of current company
#         next_shipment_date = today + datetime.timedelta( (int(shipment_day)-today.weekday()) % 7 )
#         # find the journal where default payment method checkbox is true 
# #         journal_id= journal_obj.search(cr, uid, [('default_payment_method', '=', True)], context=context)
# #         journal= journal_obj.browse(cr, uid, journal_id, context=context)[0]
#         
# #         # find all the draft stage customer invoice
# #         all_draft_invoices = inv_obj.search(cr, uid, [('state', '=', 'draft'), ('origin', 'not ilike', 'SO'),('type', '=', 'out_invoice')], context=context)
# #         all_draft_invoices_data = inv_obj.browse(cr, uid, all_draft_invoices)
# #         
# #         invoice_datas = []
# #         # filter the invoice which has source doc not start with SO
# #         for invoice in all_draft_invoices_data:
# #             if not invoice.origin.startswith('SO'):
# #                 sale_id = self.pool.get('sale.order').search(cr, uid, [('name', '=', invoice.origin), ('order_policy', '=', 'manual')], context=context)
# #                 do_id = pick_obj.search(cr, uid, [('sale_id', '=', sale_id[0])], context=context)
# #                 invoice_datas.append({'invoice_id': invoice.id, 'sale_id': sale_id, 'do_id': do_id})
# #         
# #         invoice_to_pay = []
# #         for inv in invoice_datas:
# #             do = pick_obj.browse(cr, uid, inv['do_id'], context=context)[0]
# #             do_date = datetime.datetime.strptime(do.min_date, '%Y-%m-%d %H:%M:%S').date()
# #             if do_date <= next_shipment_date:
# #                 invoice_to_pay.append(inv['invoice_id'])
#         
#         invoice_confirmed = []
#         for inv in invoice_to_pay:
#             # validate the invoice using workflow
#             try:
#                 wf_service.trg_validate(uid, 'account.invoice', inv, 'invoice_open', cr)
#                 invoice_confirmed.append(inv)
#             except:
#                 _logger.info('Invoice Fail: This invoice is failed during auto confirm wizard %s' %(inv))
#         
#         invoice_confirmed_data = inv_obj.browse(cr, uid, invoice_confirmed)
#         
#         today_date = fields.date.context_today(self, cr, uid, context=context)
#         for invoice in invoice_confirmed_data:
#             if invoice.partner_id.is_company:
#                 partner_id = invoice.partner_id.id
#             elif not invoice.partner_id.is_company and invoice.partner_id.parent_id:
#                 partner_id = invoice.partner_id.parent_id.id
#             else:
#                 partner_id = invoice.partner_id.id
#             
#             #use the multi currency
#             if journal.currency and journal.currency.id != invoice.currency_id.id:
#                 currency_id_voucher = journal.currency.id
#                 voucher_amount = self.pool.get('res.currency').compute(cr, uid, invoice.currency_id.id,
#                         journal.currency.id,
#                         invoice.amount_total, round=False, context=context)
#             elif not journal.currency and invoice.currency_id.id != invoice.company_id.currency_id.id:
#                 currency_id_voucher = invoice.company_id.currency_id.id
#                 voucher_amount = self.pool.get('res.currency').compute(cr, uid, invoice.currency_id.id, 
#                         invoice.company_id.currency_id.id,
#                          invoice.amount_total, round=False, context=context)
#             else:
#                 currency_id_voucher = invoice.currency_id.id
#                 voucher_amount = invoice.amount_total
#             
#             result = voucher_obj.onchange_partner_id(cr, uid, [], partner_id, journal.id, 
#                                                       invoice.amount_total, invoice.currency_id.id, ttype='receipt', 
#                                                       date=today_date, context=context)
#             
#             journal_data = voucher_obj.onchange_journal_voucher(cr, uid, [], line_ids=False,
#                                                                              tax_id=False, 
#                                                                              price=invoice.amount_total, 
#                                                                              partner_id=invoice.partner_id.id, 
#                                                                              journal_id=journal.id, 
#                                                                              ttype='receipt', 
#                                                                              company_id=invoice.company_id.id, 
#                                                                              context= context)
#             
#             line_cr_list = []
#             for line_dict in result['value']['line_cr_ids']:
#                 move_line = self.pool.get('account.move.line').browse(cr, uid, line_dict['move_line_id'], context)
#                 if invoice.move_id.id == move_line.move_id.id:
#                     line_dict['amount'] = voucher_amount
#                     line_cr_list.append((0, 0, line_dict))
#             
#             voucher_res = {
#                         'type': 'receipt',
#                         'reference': journal.name,
#                         'name': invoice.number,
#                         'partner_id': partner_id,
#                         'journal_id': journal.id,
#                         'account_id': journal_data['value']['account_id'],
#                         'company_id': invoice.company_id.id,
#                         'currency_id': currency_id_voucher,
#                         'date': today_date,
#                         'amount': voucher_amount,
#                         'line_cr_ids' : line_cr_list,
#                         'line_dr_ids' : False,
#                         'state': 'draft',
#                         'payment_rate': journal_data['value']['payment_rate'],
#                         'payment_rate_currency_id': journal_data['value']['payment_rate_currency_id'],
#                 }
#             #create the voucher of current invoice
#             voucher_id = voucher_obj.create(cr, uid, voucher_res, context=context)
#             voucher_line_dict =  {}
#             #add the voucher lines..
#              #post the created voucher
#             try:
#                 wf_service.trg_validate(uid, 'account.voucher', voucher_id, 'proforma_voucher', cr)
#             except:
#                 _logger.info('Voucher Validation Fail: This voucher is failed during auto create payment %s' %(voucher_id))
#         return invoice_confirmed
    
    
    def run_wizard(self, cr, uid, ids, context=None):
#         invoice_confirmed = self.auto_invoice_payment(cr, uid, context)
        for params in self.browse(cr, uid, ids, context=context):
            inv_ids = self._get_invoice_ids(cr, uid, params.shop_id.id, params.next_shipment_date, context=context)
            inv_validated = self._batch_validate_invoice(cr, uid, inv_ids, context)
            self._batch_pay_invoice(cr, uid, inv_validated, context)
        #return the list of successfully paid invoices
        return {
            'domain': "[('id','in', ["+','.join(map(str,inv_validated))+"])]",
            'name': 'Customer Invoices',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: