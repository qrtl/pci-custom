# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hide_specsheet = fields.Boolean(
        "Hide in Spec Sheet",
    )
    # part_category_id = fields.Many2one(
    #     "product.part.category",
    #     string="Part Category",
    # )
    part_categ = fields.Selection(
        [('body', 'Body'),
         ('neck', 'Neck'),
         ('hardware', 'Hardware'),
         ('pickguard', 'Pickguard'),
         ('pickup', 'Pickup'),
         ('parts', 'Parts')],
        'Part Category',
    )
