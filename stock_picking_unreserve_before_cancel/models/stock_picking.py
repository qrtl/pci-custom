# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def action_cancel(self):
        """Process do_unreserve() before action_cancel() to clear the pack operation
        records. The pack operation records will otherwise persist even when the
        cancelled picking revives with another operation type (i.e. location_id of the
        move is changed).
        """
        self.do_unreserve()
        return super(StockPicking, self).action_cancel()
