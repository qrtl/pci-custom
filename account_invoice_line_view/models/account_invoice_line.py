# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class AccountInoviceLine(models.Model):
    _inherit = 'account.invoice.line'

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
        related='invoice_id.state',
        store=True,
        string='Status'
    )
    date_invoice = fields.Date(
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
        related='invoice_id.name',
        store=True,
        string='Invoice Ref'
    )
    date_due = fields.Date(
        related='invoice_id.date_due',
        store=True,
        string='Due Date'
    )
    currency_id = fields.Many2one(
        related='invoice_id.currency_id',
        store=True,
        string='Currency'
    )
    rate = fields.Float(
        compute='_get_base_amt',
        store=True,
        string='Rate'
    )
    base_amt = fields.Monetary(
        compute='_get_base_amt',
        store=True,
        currency_field='company_currency_id',
    )
    partner_id = fields.Many2one(
        related='invoice_id.partner_id',
        string='Customer',
        store=True
    )
    

    @api.multi
    @api.depends('currency_id', 'date_invoice', 'price_subtotal')
    def _get_base_amt(self):
        for l in self:
            # set the rate 1.0 if the transaction currency is the same as the
            # company currency
            if l.company_currency_id == l.currency_id:
                l.rate = 1.0
            else:
                l.rate = l.currency_id.with_context(
                    dict(l._context or {}, date=l.date_invoice)).rate
            l.base_amt = l.price_subtotal / l.rate
