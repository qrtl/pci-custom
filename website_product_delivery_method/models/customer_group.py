# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CustomerGroup(models.Model):
    _name = 'customer.group'

    name = fields.Char(
        string="Name",
        required=True,
        copy=False,
    )
