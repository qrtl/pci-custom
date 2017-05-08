# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    procurement_calc_months = fields.Integer(
        string="No. of Months for Procurement Calc.",
        help="No. of months to consider in Product Proc. Info Update",
    )
