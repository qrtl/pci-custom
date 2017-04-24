# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    """
    override the domain so that existing configured variant can also be
    selected
    """
    product_id = fields.Many2one(
        domain=[]
    )
