# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    remarks = fields.Char(
        string="Remarks",
        compute="_compute_remarks",
        store=True,
    )

    @api.multi
    @api.depends('sale_line_ids', 'sale_line_ids.remarks')
    def _compute_remarks(self):
        for line in self:
            line.remarks = ','.join(line.sale_line_ids.filtered(
                lambda l: l.remarks).mapped('remarks'))
