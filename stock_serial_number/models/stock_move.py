# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.tools.translate import _


class stock_move(osv.osv):
    _inherit = 'stock.move'

    def action_done(self, cr, uid, ids, context=None):
        res = super(stock_move, self).action_done(cr, uid, ids, context)
        if context is None:
            context = {}
        for move in self.browse(cr, uid, ids, context):
            if (
                move.product_id.product_tmpl_id.categ_id.enforce_qty_1
                and move.product_qty > 1.0 and move.prodlot_id
            ):
                raise osv.except_osv(_('Error!'), _("Quantity of stock move should be 1"
                                                    " for product %s"
                                                    "(enforce quantity 1)."
                                                    ) % move.product_id.name)
            if (
                move.sale_line_id
                and not move.sale_line_id.serial_id
                and move.prodlot_id
            ):
                self.pool.get('sale.order.line').write(
                    cr, uid, [move.sale_line_id.id],
                    {'serial_id': move.prodlot_id.id},
                    context
                )
                invoice_line_ids = [line.id for line in move.sale_line_id.invoice_lines]
                self.pool.get('account.invoice.line').write(
                    cr, uid, invoice_line_ids,
                    {'serial_id': move.prodlot_id.id},
                    context
                )
        return res
