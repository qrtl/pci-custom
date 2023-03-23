# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ChangeSourceLocationWizard(models.TransientModel):
    _name = "change.source.location.wizard"

    source_location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Source Location',
    )

    def action_change_source_location(self):
        manufacturing_orders = self.env['mrp.production'].browse(
            self._context.get('active_ids', []))
        for order in manufacturing_orders:
            if order.location_src_id != self.source_location_id:
                order.do_unreserve()
                order.location_src_id = self.source_location_id
                for move in order.move_raw_ids:
                    move.location_id = self.source_location_id
        return
