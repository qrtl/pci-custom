# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def action_draft(self):
        moves = self.filtered(lambda m: m.state == 'cancel')
        moves.write({'state': 'draft'})

    @api.multi
    def action_cancel(self):
        """ extend the standard method to cancel linked procurements since
            the standard method has disabled cancellaton of procurements
            probably for the reason that it was not working at that time.
        """
        res = super(StockMove, self).action_cancel()
        # only do below for the moves cancelled in the standard method
        # (this does not exclude the ones that were already cancelled to begin
        # with)
        moves = self.filtered(lambda x: x.state == 'cancel')
        procurements = self.env['procurement.order'].search(
            [('move_dest_id', 'in', moves.ids)])
        if procurements:
            procurements.cancel()
        return res

    @api.multi
    def unreserve_moves(self):
        if any(move.state != 'assigned' for move in self):
            raise UserError(_('Please only select reserved stock moves.'))
        self.do_unreserve()
