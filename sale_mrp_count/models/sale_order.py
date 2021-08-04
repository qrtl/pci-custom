# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    production_ids = fields.Many2many(
        "mrp.production",
        compute="_compute_production_ids",
        string="Picking associated to this sale",
    )
    production_count = fields.Integer(
        string="Manufacturing Order", compute="_compute_production_ids",
    )

    @api.multi
    @api.depends("procurement_group_id")
    def _compute_production_ids(self):
        for order in self:
            order.production_ids = (
                self.env["mrp.production"].search(
                    [("procurement_group_id", "=", order.procurement_group_id.id)]
                )
                if order.procurement_group_id
                else []
            )
            order.production_count = len(order.production_ids)

    @api.multi
    def action_view_production(self):
        """
        This function returns an action that display existing manufacturing
        orders of given sales order ids. It can either be a in a list or in a
        form view, if there is only one delivery order to show.
        """
        action = self.env.ref("mrp.mrp_production_action").read()[0]

        productions = self.mapped("production_ids")
        if len(productions) > 1:
            action["domain"] = [("id", "in", productions.ids)]
        elif productions:
            action["views"] = [
                (self.env.ref("mrp.mrp_production_form_view").id, "form")
            ]
            action["res_id"] = productions.id
        return action
