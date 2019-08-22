# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrderInvoicePolicyReportWizard(models.TransientModel):
    _name = "sale.order.invoice.policy.report.wizard"
    _description = 'Sale Order Invoice Policy Report Wizard'

    invoice_policy = fields.Selection(
        [('order', 'Ordered quantities'),
         ('delivery', 'Delivered quantities')],
        string='Invoicing Policy',
    )

    def update_order_invoice_policy(self):
        order_id = self.env.context.get('order_id')
        if order_id:
            sale_order = self.env['sale.order'].browse(order_id)
            sale_order.update({
                'team_invoice_policy': self.invoice_policy,
            })
