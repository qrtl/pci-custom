# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_group = fields.Many2one(
        'customer.group',
        string="Customer Group",
        copy=False,
    )

    @api.model
    def create(self, vals):
        if 'customer_group' not in vals:
            default_group = self.env["customer.group"].search([
                ('name', '=', 'End-user')
            ])
            if default_group:
                vals['customer_group'] = default_group[0].id
        user = super(ResPartner, self).create(vals)
        return user
