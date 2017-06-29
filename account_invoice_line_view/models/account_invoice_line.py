# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models
from datetime import datetime
import odoo.addons.decimal_precision as dp

class AccountInoviceLine(models.Model):
    _inherit = 'account.invoice.line'
    _order = 'id desc'

    user_id = fields.Many2one(
        related='invoice_id.user_id',
        store=True,
        string='Salesperson'
    )
    
    number = fields.Char(
        related='invoice_id.number',
        store=True,
        string='Number'
    )
    
    state = fields.Selection(
        compute='_get_invoice_lines',
        related='invoice_id.state',
        store=True,
        string='Status'
    )
    
    date_invoice = fields.Date(
        compute='_get_invoice_lines',
        related='invoice_id.date_invoice',
        store=True,
        string='Invoice Date'
    )
    
    period_id = fields.Date(
        related='invoice_id.date',
        store=True,
        string='Period'
    )
    
    reference = fields.Char(
        related='invoice_id.reference',
        store=True,
        string='Invoice Ref'
    )
    
    date_due = fields.Date(
        related='invoice_id.date_due',
        store=True,
        string='Due Date'
    )
    
    currency_id = fields.Many2one(
        related='invoice_id',
        store=True,
        string='Currency'
    )
    
    rate = fields.Float(
        compute='_get_base_amt',
        store=True,
        string='Rate'
    )
    
    base_amt = fields.Float(
        compute='_get_base_amt',
        store=True,
        digits_compute=dp.get_precision('Account')
    )
    
    partner_id = fields.Many2one(
        compute='_get_invoice_lines',
        related='invoice_id.partner_id',
        string='Customer',
        store=True
    )
    
    def _get_base_amt(self, cr, uid, ids, args, context=None):
        res = {}
        for invoice_line in self:
            curr_amt = invoice_line.price_subtotal
            # set the rate 1.0 if the transaction currency is the same as the base currency
            if invoice_line.company_id.currency_id == invoice_line.currency_id:
                rate = 1.0
            else:
                invoice_obj = self.pool.get('account.invoice')
                invoice_date = invoice_obj.read(cr, uid, invoice_line.invoice_id.id, ['date_invoice'])['date_invoice']
                if invoice_date:
                    invoice_date_datetime = datetime.strptime(invoice_date, '%Y-%m-%d')
                else:
                    today = context.get('date', datetime.today().strftime('%Y-%m-%d'))
                    invoice_date_datetime = datetime.strptime(today, '%Y-%m-%d')

                rate_obj = self.pool['res.currency.rate']
                rate_id = rate_obj.search(cr, uid, [
                    ('currency_id', '=', invoice_line.currency_id.id),
                    ('name', '<=', invoice_date_datetime),
                    # not sure for what purpose 'currency_rate_type_id' field exists in the table, but keep this line just in case
                    ('currency_rate_type_id', '=', None)
                    ], order='name desc', limit=1, context=context)
                if rate_id:
#                     rate = rate_obj.read(cr, uid, rate_rec[0], ['rate'], context=context)['rate']
                    rate = rate_obj.browse(cr, uid, rate_id, context=context)[0].rate
                else:
                    rate = 1.0
            res[invoice_line.id] = {
                'rate': rate,
                'base_amt': curr_amt / rate,
                }
        return res

    def _get_invoice_lines(self, cr, uid, ids, context=None):
        invoice_line_ids = []
        for invoice in self.browse(cr, uid, ids, context=context):
            invoice_line_ids += self.pool.get('account.invoice.line').search(cr, uid, [('invoice_id.id', '=', invoice.id)], context=context)
        return invoice_line_ids

    def init(self):
        # to be executed only when installing the module.  update "stored" fields 
        self._cr.execute("update account_invoice_line line \
                    set state = inv.state, date_invoice = inv.date_invoice, partner_id = inv.partner_id \
                    from account_invoice inv \
                    where line.invoice_id = inv.id")
