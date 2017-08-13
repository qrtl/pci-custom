# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    expected_date = fields.Datetime(
        compute='_get_expected_date',
        string='Commitment Date',
        store=True,
    )

    @api.multi
    @api.depends('requested_date', 'commitment_date')
    def _get_expected_date(self):
        for order in self:
            order.expected_date = order.requested_date if order.requested_date\
                else order.commitment_date
