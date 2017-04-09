# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    product_type = fields.Selection(
        related='product_id.product_tmpl_id.type',
        store=True,
        string="Product Type"
    )
