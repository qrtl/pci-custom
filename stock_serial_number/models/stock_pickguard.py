# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockPickguard(models.Model):
    _name = 'stock.pickguard'

    name = fields.Char(required=True)
