# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
