# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    expected_date = fields.Date(
        readonly=True,
        store=True,
        string='Expected Date',
        compute='_compute_expected_date'
    )

    @api.multi
    @api.depends('requested_date', 'commitment_date')
    def _compute_expected_date(self):
        for order in self:
            if order.requested_date:
                order.expected_date = order.requested_date
            else:
                order.expected_date = order.commitment_date
