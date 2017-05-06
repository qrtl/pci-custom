# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = "product.product"

    avg_qty_needed = fields.Float(
        'Average Qty Needed (per Month)',
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True
    )
    avg_qty_adj = fields.Float(
        'Adjusted Qty',
        digits=dp.get_precision('Product Unit of Measure'),
    )
    avg_qty_adj_comp = fields.Float(
        'Average Qty Needed (Adjusted)',
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True
    )
    proc_lt_calc = fields.Float(
        'Procurement LT (Calculated)',
        readonly=True
    )
    proc_lt_manu = fields.Float(
        'Procurement LT (Manual)'
    )
    qty_suggested = fields.Float(
        compute="_compute_qty",
        string='Suggested Stock Qty',
        digits=dp.get_precision('Product Unit of Measure'),
    )
    qty_variance = fields.Float(
        compute="_compute_qty",
        string='Variance',
        digits=dp.get_precision('Product Unit of Measure'),
    )


    # def _compute_qty(self, cr, uid, ids, field_names, args, context=None):
    #     res = {}
    #     prod_ids = self.search(cr, uid, [])
    #     for prod in self.browse(cr, uid, prod_ids, context=context):
    #         if prod.avg_qty_adj_comp:
    #             avg_qty = prod.avg_qty_adj_comp
    #         elif prod.avg_qty_adj:
    #             avg_qty = prod.avg_qty_adj
    #         else:
    #             avg_qty = prod.avg_qty_needed
    #         if prod.proc_lt_manu:
    #             proc_lt = prod.proc_lt_manu
    #         else:
    #             proc_lt = prod.proc_lt_calc
    #         qty_suggested = avg_qty * proc_lt
    #         qty_variance = prod.qty_available + prod.incoming_qty - qty_suggested
    #         res[prod.id] = {
    #             'qty_suggested': qty_suggested,
    #             'qty_variance': qty_variance,
    #         }
    #     return res

    @api.multi
    def _compute_qty(self):
        for prod in self:
            if prod.avg_qty_adj_comp:
                avg_qty = prod.avg_qty_adj_comp
            elif prod.avg_qty_adj:
                avg_qty = prod.avg_qty_adj
            else:
                avg_qty = prod.avg_qty_needed
            if prod.proc_lt_manu:
                proc_lt = prod.proc_lt_manu
            else:
                proc_lt = prod.proc_lt_calc
            # qty_suggested = avg_qty * proc_lt
            # qty_variance = prod.qty_available + prod.incoming_qty - qty_suggested
            prod.qty_suggested = avg_qty * proc_lt
            prod.qty_variance = prod.qty_available + prod.incoming_qty - \
                                prod.qty_suggested
