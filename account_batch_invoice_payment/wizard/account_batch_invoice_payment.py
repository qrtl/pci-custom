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
from openerp.exceptions import Warning
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
import pytz
from openerp import SUPERUSER_ID
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
            shop = self.pool.get('sale.shop').browse(cr, uid, [shop_id])[0]
            next_shipment_date = self.pool.get('sale.shop').get_shipment_date(cr, uid, shop_id=shop.id, context=context)
            res['value'] = {'next_shipment_date': next_shipment_date.strftime(DEFAULT_SERVER_DATE_FORMAT)}
        return res


    def _get_default_shop(self, cr, uid, context=None):
        shop_obj = self.pool.get('sale.shop')
        shop_ids = shop_obj.search(cr, uid, [('invoice_batch_process_default','=',True)])
        if shop_ids:
            for shop in shop_obj.browse(cr, uid, shop_ids, context=context):
                shop_id = shop.id
            return shop_id
    
    _defaults = {
         'shop_id': _get_default_shop
    }


    def _get_journal(self, cr, uid, sale_name, context=None):
        res = False
        sale_obj = self.pool.get('sale.order')
        sale_ids = sale_obj.search(cr, uid, [('name','=',sale_name)])
        for sale in sale_obj.browse(cr, uid, sale_ids, context=context):
            if sale.payment_method_id and sale.payment_method_id.journal_id:
                res = sale.payment_method_id.journal_id
        return res


    def _get_user_tz_date(self, cr, uid, date, context=None):
        user = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid)
        if user.partner_id.tz:
            tz = pytz.timezone(user.partner_id.tz)
        else:
            tz = pytz.utc
        res = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        res = pytz.utc.localize(res).astimezone(tz)
        return res


    def _get_invoice_ids(self, cr, uid, shop_id, next_shipment_date, context=None):
        inv_obj = self.pool.get('account.invoice')
        sale_obj = self.pool.get('sale.order')
        pick_obj = self.pool.get('stock.picking')
        draft_inv_ids = inv_obj.search(cr, uid,
            [('state','=','draft'),
             ('type','=','out_invoice'),
             ('amount_total','>',0)])
        res = []
        # filter invoices with shop_id and next_shipment_date
        for inv in inv_obj.browse(cr, uid, draft_inv_ids):
            sale_ids = sale_obj.search(cr, uid,
                    [('name', '=', inv.origin),
                     ('order_policy', '=', 'manual'),
                     ('shop_id', '=', shop_id),
                     ], context=context)
            if sale_ids:
                min_pick_date = datetime(9999, 12, 31).date()
                for sale in sale_obj.browse(cr, uid, sale_ids):
                    if sale.payment_method_id and sale.payment_method_id.journal_id:
                        pick_ids = pick_obj.search(cr, uid, [('sale_id', '=', sale.id)], context=context)
                        if pick_ids:
                            for pick in pick_obj.browse(cr, uid, pick_ids, context=context):
                                pick_date = self._get_user_tz_date(cr, uid, pick.min_date, context=context).date()
                                if pick_date < min_pick_date:
                                    min_pick_date = pick_date
                            if min_pick_date <= next_shipment_date:
                                res.append(inv.id)
        return res

    
    def _batch_validate_invoice(self, cr, uid, inv_ids, next_shipment_date, context=None):
        inv_obj = self.pool.get('account.invoice')
        inv_validated = []
        for inv_id in inv_ids:
            inv_obj.write(cr, uid, inv_id, {'date_invoice': next_shipment_date.strftime(DEFAULT_SERVER_DATE_FORMAT)})
            try:
                netsvc.LocalService('workflow').trg_validate(uid, 'account.invoice', inv_id, 'invoice_open', cr)
                # it seems the "except" is not raised in case validation fails due to period not being defined
                # because of this, update on "inv_validated" is moved at the bottom of the loop
#                 inv_validated.append(inv_id)
            except:
                _logger.info('Invoice Fail: This invoice is failed during auto confirm wizard %s' %(inv_id))
            if inv_obj.browse(cr, uid, [inv_id], context=context)[0].state == 'open':
                inv_validated.append(inv_id)
        return inv_validated
    
    
    def _batch_pay_invoice(self, cr, uid, inv_validated, context=None):
        inv_obj = self.pool.get('account.invoice')
        voucher_obj = self.pool.get('account.voucher')
        for inv in inv_obj.browse(cr, uid, inv_validated):
            if inv.partner_id.is_company:
                partner_id = inv.partner_id.id
            elif not inv.partner_id.is_company and inv.partner_id.parent_id:
                partner_id = inv.partner_id.parent_id.id
            else:
                partner_id = inv.partner_id.id
            
            journal = self._get_journal(cr, uid, inv.origin, context=context)
            if journal:
                # support multi currency
                curr_obj = self.pool.get('res.currency')
                if journal.currency and journal.currency.id != inv.currency_id.id:
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
                            journal.id, inv.amount_total,
                            inv.currency_id.id, ttype='receipt',
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


    def batch_process_invoice_auto(self, cr, uid, context=None):
        shop_obj = self.pool.get('sale.shop')
        shop_ids = shop_obj.search(cr, uid, [('auto_pay_invoice','=',True)])
        for shop in shop_obj.browse(cr, uid, shop_ids, context=context):
            next_shipment_date = shop_obj.get_shipment_date(cr, uid, shop_id=shop.id, context=context)
            if self.pool.get('account.period').find(cr, uid, next_shipment_date, context=context):
                inv_ids = self._get_invoice_ids(cr, uid, shop.id, next_shipment_date, context=context)
                inv_validated = self._batch_validate_invoice(cr, uid, inv_ids, next_shipment_date, context)
                # disable batch payment for now (OSCG)
                # self._batch_pay_invoice(cr, uid, inv_validated, context)

    
    def run_wizard(self, cr, uid, ids, context=None):
        for params in self.browse(cr, uid, ids, context=context):
            next_shipment_date = datetime.strptime(params.next_shipment_date, '%Y-%m-%d').date()
            if self.pool.get('account.period').find(cr, uid, next_shipment_date, context=context):
                inv_ids = self._get_invoice_ids(cr, uid, params.shop_id.id, next_shipment_date, context=context)
                inv_validated = self._batch_validate_invoice(cr, uid, inv_ids, next_shipment_date, context)
                # disable batch payment for now (OSCG)
                # self._batch_pay_invoice(cr, uid, inv_validated, context)
        return {
            'domain': "[('id','in', ["+','.join(map(str,inv_validated))+"])]",
            'name': 'Customer Invoices',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: