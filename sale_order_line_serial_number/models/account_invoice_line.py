# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    serial_number = fields.Char(
        string='Serial Number',
        compute='_compute_serial_number',
    )

    @api.multi
    def _compute_serial_number(self):
        for line in self:
            serial_number_list = []
            for order_line in line.sale_line_ids:
                serial_number_list.append(order_line.serial_number)
            line.serial_number = ','.join(serial_number_list)
