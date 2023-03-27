# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockNeck(models.Model):
    _name = 'stock.neck'

    name = fields.Char(required=True)
