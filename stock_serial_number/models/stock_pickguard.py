# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockPickguard(models.Model):
    _name = 'stock.pickguard'

    name = fields.Char(required=True)
