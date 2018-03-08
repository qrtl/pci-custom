# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'


    @api.multi
    def cancel(self):
        super(AccountPayment, self).cancel()
        for rec in self:
            rec.move_name = False
