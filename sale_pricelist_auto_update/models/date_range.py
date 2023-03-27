# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DateRange(models.Model):
    _inherit = "date.range"

    is_fiscal_year = fields.Boolean(
        related="type_id.is_fiscal_year", store=True, string="Fiscal Year",
    )
