# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    customer_remarks = fields.Text(string="Customer Remarks", readonly=True)
