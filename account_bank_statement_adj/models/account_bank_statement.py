# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    @api.multi
    def button_cancel_reconciliation(self):
        super(AccountBankStatementLine, self).button_cancel_reconciliation()
        for st_line in self:
            st_line.move_name = False
