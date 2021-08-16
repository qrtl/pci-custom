# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class Users(models.Model):
    _inherit = "res.users"

    salesperson_select = fields.Boolean(
        string="Salesperson Setectable",
        help="Indicates the salesperson to be selected in sales order",
    )

    @api.multi
    def toggle_salesperson(self):
        for record in self:
            record.salesperson_select = not record.salesperson_select
