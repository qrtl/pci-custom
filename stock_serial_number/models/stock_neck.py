# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockNeck(models.Model):
    _name = 'stock.neck'

    name = fields.Char(required=True)
