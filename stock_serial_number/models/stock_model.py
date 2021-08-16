# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockModel(models.Model):
    _name = "stock.model"
    _order = "sequence"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=5)
