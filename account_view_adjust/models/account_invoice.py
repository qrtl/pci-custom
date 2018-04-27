# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError
from odoo import models, fields, api, _


class AccountInovice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_cancel(self):
        if self.filtered(
                lambda inv: inv.state not in ['proforma2', 'draft', 'open']
                and inv.state == "paid" and inv.amount_total != 0):
            raise UserError(_("Invoice must be in draft, Pro-forma or open "
                              "state or the invoice amount is 0 in order to "
                              "be cancelled."))
        return self.action_cancel()
