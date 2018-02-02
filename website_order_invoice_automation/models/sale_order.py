# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    auto_invoice = fields.Boolean(
        related='team_id.auto_invoice',
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

    def action_check_invoiceable_order(self):
        confirm_sale_order_list = self.search([
            ('state', '=', 'sale'),
            ('auto_invoice', '=', True)
        ])
        for sale_order in confirm_sale_order_list:
            if sale_order._is_invoiceable():
                sale_order._generate_and_validate_invoice()


    def _is_invoiceable(self):
        invoiceable_order = False
        for order_line in self.order_line:
            # Check whether is invoiceable lines
            if not invoiceable_order and order_line.qty_to_invoice > 0:
                invoiceable_order = True
            # Check whether the order is fully delivered, return False if
            # any line is not fully delivered (except service product /
            # shipping cost)
            if (order_line._get_delivered_qty() < order_line.product_uom_qty) \
                    and order_line.product_id.type != 'service' \
                    and not order_line.product_id.is_shipping_cost:
                return False
        return True if invoiceable_order else False
