# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


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

    def _compute_partner_id(self):
        for order in self:
            if order.procurement_group_id:
                order.partner_id = order.procurement_group_id.partner_id
