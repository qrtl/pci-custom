# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DateRangeType(models.Model):
    _inherit = "date.range.type"

    is_fiscal_year = fields.Boolean(string="Fiscal Year",)
