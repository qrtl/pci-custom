# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    auto_invoice = fields.Boolean(
        related='order_id.team_id.auto_invoice',
        store=True,
    )

    @api.depends('qty_invoiced', 'qty_delivered', 'product_uom_qty',
                 'order_id.state', 'order_id.team_id.invoice_policy')
    def _get_to_invoice_qty(self):
        for line in self:
            invoice_policy = line.order_id.team_id.invoice_policy or \
                             line.product_id.invoice_policy
            if line.order_id.state in ['sale', 'done']:
                if invoice_policy == 'order':
                    line.qty_to_invoice = line.product_uom_qty - \
                                          line.qty_invoiced
                else:
                    line.qty_to_invoice = line.qty_delivered - \
                                          line.qty_invoiced
            else:
                line.qty_to_invoice = 0

    def action_check_invoiceable_line(self):
        invoiceable_order_lines = self.search([
            ('qty_to_invoice', '>', '0'),
            ('state', '=', 'sale'),
            ('auto_invoice', '=', True)
        ])
        for order_line in invoiceable_order_lines:
            if order_line.qty_to_invoice > 0:
                order_line.order_id._generate_and_validate_invoice()
