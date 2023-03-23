# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def post_inventory(self):
        for order in self:
            if order.move_raw_ids.filtered(
                lambda x: x.state not in ['assigned', 'done', 'cancel']
            ):
                raise UserError(_(
                    "Please make sure that stock is reserved for all "
                    "components before posting inventory."
                ))
        return super(MrpProduction, self).post_inventory()
