# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_available_location = fields.Float(
        # 'Quantity on Hand Location',
        related="product_id.qty_available_location",
        # digits=dp.get_precision('Product Unit of Measure'),
    )
