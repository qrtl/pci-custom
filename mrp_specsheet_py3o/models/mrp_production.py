# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    partner_id = fields.Many2one(
        "res.partner",
        compute="_compute_partner_id",
        string="Customer",
        help="The customer whom this manufacturing order is intended for. The "
             "value is taken from originating sales order in case the "
             "manufacturing order was generated based on Make to Order.",
    )
    special_instruction = fields.Char(
        compute="_compute_special_instruction",
        string="Special Instruction",
    )

    def _compute_partner_id(self):
        for order in self:
            if order.procurement_group_id:
                order.partner_id = order.procurement_group_id.partner_id

    def _compute_special_instruction(self):
        for order in self:
            # .mapped() removes duplicates if any
            tags = order.move_raw_ids.mapped('product_id.special_tag_ids')
            tag_desc = '; '.join(tags.mapped('name')) if tags else False
            order.special_instruction = '; '.join(filter(None, [order.remarks,
                                                                tag_desc]))
