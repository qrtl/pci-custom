# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api,models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.multi
    def write(self, values):
        res = super(PurchaseOrderLine, self).write(values)
        lines = self.filtered(lambda l: l.order_id.state == 'purchase')
        if 'price_unit' in values:
            for line in lines:
                moves = line.move_ids.filtered(lambda s: s.state not in ('cancel', 'done') and s.product_id == line.product_id)
                moves.write({'price_unit': line._get_stock_move_price_unit()})
