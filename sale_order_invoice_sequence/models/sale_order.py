# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        invoice_ids = super(SaleOrder, self).action_invoice_create(grouped=grouped, final=final)
        invoices = self.env["account.invoice"].browse(invoice_ids)
        for invoice in invoices:
            seq = 1
            ordered_lines = invoice.invoice_line_ids.sorted(
                key=lambda l: (
                    l.sale_line_ids and l.sale_line_ids[0].order_id.id or 0,
                    l.sale_line_ids and l.sale_line_ids[0].sequence or 0,
                    l.id,
                )
            )
            for line in ordered_lines:
                line.sequence = seq
                seq += 1
        return invoice_ids
