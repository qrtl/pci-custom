# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    remarks = fields.Char(
        readonly=True,
        copy=False,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        string="Remarks",
    )
