# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    remarks = fields.Char(string="Remarks",)
