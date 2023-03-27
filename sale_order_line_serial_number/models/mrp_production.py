# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    serial_number = fields.Char(
        string='Serial Number',
    )
