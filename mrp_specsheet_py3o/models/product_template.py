# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hide_specsheet = fields.Boolean(
        "Hide in Spec Sheet",
        help="If selected, the product will not show in spec sheet print.",
    )
    part_categ = fields.Selection(
        [('body', 'Body'),
         ('neck', 'Neck'),
         ('hardware', 'Hardware'),
         ('pickguard', 'Pickguard'),
         ('pickup', 'Pickup'),
         ('parts', 'Parts')],
        'Part Category',
        help="The selection here will affect where in printed spec sheet the "
             "product is presented.",
    )
