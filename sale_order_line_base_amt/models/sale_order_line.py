# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='order_id.company_id.currency_id',
        store=True,
        readonly=True,
        string='Company Currency',
    )
    base_amt = fields.Monetary(
        compute='_get_base_amt',
        store=True,
        currency_field='company_currency_id',
        string='Base Amount',
    )

    @api.multi
    @api.depends('company_currency_id', 'order_id.date_order',
                 'price_subtotal')
    def _get_base_amt(self):
        for record in self:
            # set the rate 1.0 if the transaction currency is the same as the
            # company currency
            if record.company_currency_id == record.currency_id:
                record.rate = 1.0
            else:
                record.rate = record.currency_id.with_context(
                    dict(record._context or {}, date=record.order_id.date_order)).rate
            record.base_amt = record.price_subtotal / record.rate
