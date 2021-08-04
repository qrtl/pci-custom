# -*- coding: utf-8 -*-

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    # product_id = fields.Many2one(domain=[('config_ok', '=', False)])
    # remove domain because configurable product cannot be selected in stock
    # moves (inventory transfer), otherwise.
    product_id = fields.Many2one(domain=[])
