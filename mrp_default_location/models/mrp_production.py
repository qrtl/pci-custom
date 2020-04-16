# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # add properties to standard field
    location_src_id = fields.Many2one(
        compute='_update_location_src_id',
        store=True,
    )

    @api.multi
    @api.depends('product_id')
    def _update_location_src_id(self):
        self.ensure_one()
        if self.product_id and \
                self.product_id.product_tmpl_id.mrp_location_src_id:
            self.location_src_id = \
                self.product_id.product_tmpl_id.mrp_location_src_id
        else:
            self.location_src_id = self._get_default_location_src_id()
