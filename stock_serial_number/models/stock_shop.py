# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockShop(models.Model):
    _name = "stock.shop"

    name = fields.Char(required=True)
