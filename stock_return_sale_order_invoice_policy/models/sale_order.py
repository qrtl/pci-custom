# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    update_invoice_policy = fields.Boolean(
        string='Manual Update Invoice Policy',
        default=False,
    )

    @api.multi
    def update_order_invoice_policy(self):
        view_form = self.env.ref(
            'stock_return_sale_order_invoice_policy.sale_order_invoice_policy_report_wizard_form')
        return {
            'name': _("Update Order's Invoice Policy"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sale.order.invoice.policy.report.wizard',
            'views': [(view_form.id, 'form')],
            'view_id': view_form.id,
            'target': 'new',
            'context': dict(
                self.env.context,
                order_id=self.id,
            ),
        }
