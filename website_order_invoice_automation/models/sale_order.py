# -*- coding: utf-8 -*-
# Copyright 2018-2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    team_invoice_policy = fields.Selection(
        [('order', 'Ordered quantities'),
         ('delivery', 'Delivered quantities')],
        string='Invoicing Policy',
    )

    def _generate_and_validate_invoice(self):
        ctx_company = {'company_id': self.company_id.id,
                       'force_company': self.company_id.id}
        created_invoice = self.with_context(
            **ctx_company).action_invoice_create()
        created_invoice = self.env['account.invoice'].browse(
            created_invoice).with_context(**ctx_company)

        if created_invoice:
            _logger.info('Auto-generated invoice %s (ID %s) for %s (ID %s)',
                         created_invoice.name, created_invoice.id,
                         self.name, self.id)

            created_invoice.action_invoice_open()
        else:
            _logger.warning('Could not auto-generate invoice for %s (ID %s)',
                            self.name, self.id)

    def _is_invoiceable(self):
        # Check whether there is invoiceable line
        for order_line in self.order_line:
            if order_line.qty_to_invoice > 0:
                return True
        return False

    @api.multi
    def write(self, vals):
        if 'team_id' in vals:
            invoice_policy = False
            if vals['team_id']:
                invoice_policy = self.env['crm.team'].browse(
                    vals['team_id']).invoice_policy
            vals['team_invoice_policy'] = invoice_policy
        return super(SaleOrder, self).write(vals)

    @api.model
    def create(self, vals):
        if 'team_id' in vals:
            invoice_policy = False
            if vals['team_id']:
                invoice_policy = self.env['crm.team'].browse(
                    vals['team_id']).invoice_policy
            vals['team_invoice_policy'] = invoice_policy
        return super(SaleOrder, self).create(vals)
