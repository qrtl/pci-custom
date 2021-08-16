# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hide_specsheet = fields.Boolean(
        "Hide in Spec Sheet",
        help="If selected, the product will not show in the body part of the "
        "printed spec sheet.",
    )
    part_categ = fields.Selection(
        [
            ("body", "Body"),
            ("neck", "Neck"),
            ("hardware", "Hardware"),
            ("pickguard", "Pickguard"),
            ("parts", "Parts"),
        ],
        "Part Category",
        help="The selection here will affect where in printed spec sheet the "
        "product is presented.",
    )
    special_tag_ids = fields.Many2many(
        "product.special.tag",
        column1="product_tmpl_id",
        column2="special_tag_id",
        string="Special Tags",
        help="Input value here, together with Remarks, will form Special "
        "Instruction in printed spec sheet.",
    )
    short_desc = fields.Char(
        "Short Description",
        help="Short description to show for the tear-off part in spec sheet.",
    )
