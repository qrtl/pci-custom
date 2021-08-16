# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class UpdatePricelisrWizard(models.TransientModel):
    _name = "update.pricelist.wizard"

    date_range = fields.Many2one(
        comodel_name="date.range", string="Date Range", required=True,
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner",)

    @api.multi
    def action_update_pricelist(self):
        self.env["res.partner"].reset_partner_pricelist(
            self.date_range, self.partner_id
        )
        return True
