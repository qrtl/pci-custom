# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def change_source_location(self):
        form_id = self.env.ref(
            'mrp_change_source_location.change_source_location_wizard_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Change Source Location',
            'res_model': 'change.source.location.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {},
            'target': 'new',
        }
