# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class StockModel(models.Model):
    _name = 'stock.model'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=5)
