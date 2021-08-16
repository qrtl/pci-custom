# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models
from odoo.addons import decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    lot_id = fields.Many2one(
        comodel_name="stock.production.lot", string="Serial Number", copy=False,
    )
    standard_price = fields.Float(
        related="lot_id.standard_price",
        string="Cost Price",
        digits_compute=dp.get_precision("Product Price"),
        groups="base.group_user",
        copy=False,
    )
