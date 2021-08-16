# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    mrp_location_src_id = fields.Many2one(
        comodel_name="stock.location",
        domain=[("usage", "=", "internal")],
        string="Manufacturing Default Source Location",
    )
