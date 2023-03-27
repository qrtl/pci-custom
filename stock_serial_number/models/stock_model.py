# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockModel(models.Model):
    _name = 'stock.model'
    _order = 'sequence'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=5)
