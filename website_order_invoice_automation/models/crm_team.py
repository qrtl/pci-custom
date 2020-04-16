# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    invoice_policy = fields.Selection(
        [('order', 'Ordered quantities'),
         ('delivery', 'Delivered quantities')],
        string='Invoicing Policy',
        help='Ordered Quantity: Invoice based on the quantity the customer '
             'ordered.\n Delivered Quantity: Invoiced based on the quantity '
             'the vendor delivered (time or deliveries).',
    )
    auto_invoice = fields.Boolean(
        string='Auto Creation and Validation of Invoices',
        default=False,
    )
