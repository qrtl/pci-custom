# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.addons.l10n_us_check_printing.report.print_check import report_print_check, INV_LINES_PER_STUB


def get_pages(self, payment):
    """ Returns the data structure used by the template : a list of dicts containing what to print on pages.
    """
    stub_pages = self.make_stub_pages(payment)
    multi_stub = payment.company_id.us_check_multi_stub
    pages = []
    for i in range(0, stub_pages != None and len(stub_pages) or 1):
        pages.append({
            'sequence_number': payment.check_number
            if (payment.journal_id.check_manual_sequencing and payment.check_number != 0)
            else False,
            'payment_date': payment.payment_date,
            # <<< QTL ADD
            # Add partner_id to the template data to display the address
            'partner_id': payment.partner_id,
            # >>> QTL ADD
            'partner_name': payment.partner_id.name,
            'currency': payment.currency_id,
            'amount': payment.amount if i == 0 else 'VOID',
            'amount_in_word': self.fill_line(payment.check_amount_in_words) if i == 0 else 'VOID',
            'memo': payment.communication,
            'stub_cropped': not multi_stub and len(payment.invoice_ids) > INV_LINES_PER_STUB,
            # If the payment does not reference an invoice, there is no stub line to display
            'stub_lines': stub_pages != None and stub_pages[i],
        })
    return pages


class ReportPrintCheckHookGetPages(models.AbstractModel):
    _name = "report.print.check.hook.get.pages"
    _description = "Provide hook point for get_pages method"

    def _register_hook(self):
        report_print_check.get_pages = get_pages
        return super(ReportPrintCheckHookGetPages, self)._register_hook()
