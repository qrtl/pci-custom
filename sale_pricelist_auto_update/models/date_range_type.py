# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class DateRangeType(models.Model):
    _inherit = "date.range.type"

    is_fiscal_year = fields.Boolean(
        string='Fiscal Year',
    )
