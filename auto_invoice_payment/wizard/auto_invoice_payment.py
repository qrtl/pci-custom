# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc
import datetime
import logging
_logger = logging.getLogger(__name__)

class account_journal(osv.osv):
    _inherit = 'account.journal'
    
    _columns = {
        'default_payment_method': fields.boolean('Default Payment Method')
    }

class invoice_payment_wizard(osv.osv_memory):
    _name = 'invoice.payment.wizard'

    def auto_invoice_payment(self, cr, uid, context=None):
        if not context:
            context = {}
        shop_obj = self.pool.get('sale.shop')
        journal_obj = self.pool.get('account.journal')
        inv_obj = self.pool.get('account.invoice')
        pick_obj = self.pool.get('stock.picking')
        voucher_obj = self.pool.get('account.voucher')
        
        wf_service = netsvc.LocalService('workflow')
        user = self.pool.get('res.users').browse(cr, uid, uid)
        company_id = user.company_id.id
        
        #find the shop of current company
        shop_id = shop_obj.search(cr, uid, [('company_id', '=', company_id)], context=context)[0]
        shop = shop_obj.browse(cr, uid, shop_id, context=context)
        shipment_day = shop.shipment_day
        
        today = datetime.date.today()
        #find the date of next shipment day defined on sale shop of current company
        next_shipment_date = today + datetime.timedelta( (int(shipment_day)-today.weekday()) % 7 )
        #find the journal where default payment method checkbox is true 
        journal_id= journal_obj.search(cr, uid, [('default_payment_method', '=', True)], context=context)
        journal= journal_obj.browse(cr, uid, journal_id, context=context)[0]
        
        #find the all the draft stage customer invoice
        all_draft_invoices = inv_obj.search(cr, uid, [('state', '=', 'draft'), ('origin', 'not ilike', 'SO'),('type', '=', 'out_invoice')], context=context)
        all_draft_invoices_data = inv_obj.browse(cr, uid, all_draft_invoices)
        
        invoice_datas = []
        #filter the invoice which has source doc not start with SO
        for invoice in all_draft_invoices_data:
            if not invoice.origin.startswith('SO'):
                sale_id = self.pool.get('sale.order').search(cr, uid, [('name', '=', invoice.origin), ('order_policy', '=', 'manual')], context=context)
                do_id = pick_obj.search(cr, uid, [('sale_id', '=', sale_id[0])], context=context)
                invoice_datas.append({'invoice_id': invoice.id, 'sale_id': sale_id, 'do_id': do_id})
        
        invoice_to_pay = []
        for inv in invoice_datas:
            do = pick_obj.browse(cr, uid, inv['do_id'], context=context)[0]
            do_date = datetime.datetime.strptime(do.min_date, '%Y-%m-%d %H:%M:%S').date()
            if do_date <= next_shipment_date:
                invoice_to_pay.append(inv['invoice_id'])
        
        invoice_confirmed = []
        for inv in invoice_to_pay:
            #validate the invoice using workflow
            try:
                wf_service.trg_validate(uid, 'account.invoice', inv, 'invoice_open', cr)
                invoice_confirmed.append(inv)
            except:
                _logger.info('Invoice Fail: This invoice is failed during auto confirm wizard %s' %(inv))
        
        invoice_confirmed_data = inv_obj.browse(cr, uid, invoice_confirmed)
        
        today_date = fields.date.context_today(self, cr, uid, context=context)
        for invoice in invoice_confirmed_data:
            if invoice.partner_id.is_company:
                partner_id = invoice.partner_id.id
            elif not invoice.partner_id.is_company and invoice.partner_id.parent_id:
                partner_id = invoice.partner_id.parent_id.id
            else:
                partner_id = invoice.partner_id.id
            
            #use the multi currency
            if journal.currency and journal.currency.id != invoice.currency_id.id:
                currency_id_voucher = journal.currency.id
                voucher_amount = self.pool.get('res.currency').compute(cr, uid, invoice.currency_id.id,
                        journal.currency.id,
                        invoice.amount_total, round=False, context=context)
            elif not journal.currency and invoice.currency_id.id != invoice.company_id.currency_id.id:
                currency_id_voucher = invoice.company_id.currency_id.id
                voucher_amount = self.pool.get('res.currency').compute(cr, uid, invoice.currency_id.id, 
                        invoice.company_id.currency_id.id,
                         invoice.amount_total, round=False, context=context)
            else:
                currency_id_voucher = invoice.currency_id.id
                voucher_amount = invoice.amount_total
            
            result = voucher_obj.onchange_partner_id(cr, uid, [], partner_id, journal.id, 
                                                      invoice.amount_total, invoice.currency_id.id, ttype='receipt', 
                                                      date=today_date, context=context)
            
            journal_data = voucher_obj.onchange_journal_voucher(cr, uid, [], line_ids=False,
                                                                             tax_id=False, 
                                                                             price=invoice.amount_total, 
                                                                             partner_id=invoice.partner_id.id, 
                                                                             journal_id=journal.id, 
                                                                             ttype='receipt', 
                                                                             company_id=invoice.company_id.id, 
                                                                             context= context)
            
            line_cr_list = []
            for line_dict in result['value']['line_cr_ids']:
                move_line = self.pool.get('account.move.line').browse(cr, uid, line_dict['move_line_id'], context)
                if invoice.move_id.id == move_line.move_id.id:
                    line_dict['amount'] = voucher_amount
                    line_cr_list.append((0, 0, line_dict))
            
            voucher_res = {
                        'type': 'receipt',
                        'reference': journal.name,
                        'name': invoice.number,
                        'partner_id': partner_id,
                        'journal_id': journal.id,
                        'account_id': journal_data['value']['account_id'],
                        'company_id': invoice.company_id.id,
                        'currency_id': currency_id_voucher,
                        'date': today_date,
                        'amount': voucher_amount,
                        'line_cr_ids' : line_cr_list,
                        'line_dr_ids' : False,
                        'state': 'draft',
                        'payment_rate': journal_data['value']['payment_rate'],
                        'payment_rate_currency_id': journal_data['value']['payment_rate_currency_id'],
                }
            #create the voucher of current invoice
            voucher_id = voucher_obj.create(cr, uid, voucher_res, context=context)
            voucher_line_dict =  {}
            #add the voucher lines..
             #post the created voucher
            try:
                wf_service.trg_validate(uid, 'account.voucher', voucher_id, 'proforma_voucher', cr)
            except:
                _logger.info('Voucher Validation Fail: This voucher is failed during auto create payment %s' %(voucher_id))
        return invoice_confirmed
    
    
    def run_wizard(self, cr, uid, ids, context=None):
        invoice_confirmed = self.auto_invoice_payment(cr, uid, context)
        #return the list of successfully paid invoices
        return {
            'domain': "[('id','in', ["+','.join(map(str,invoice_confirmed))+"])]",
            'name': 'Customer Invoices',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: