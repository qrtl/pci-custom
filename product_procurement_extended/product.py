# -*- coding: utf-8 -*-
# import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import logging

class product_product(osv.osv):
    _inherit = "product.product"

    def _compute_qty(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        prod_ids = self.search(cr, uid, [])
        for prod in self.browse(cr, uid, prod_ids, context=context):
            if prod.proc_lt_manu:
                qty_suggested = prod.avg_qty_needed * prod.proc_lt_manu
            else:
                qty_suggested = prod.avg_qty_needed * prod.proc_lt_calc
            qty_variance = prod.qty_available + prod.incoming_qty - qty_suggested
            res[prod.id] = {
                'qty_suggested': qty_suggested,
                'qty_variance': qty_variance,
                }
        return res
    
    _columns = {
       'avg_qty_needed': fields.float('Average Qty Needed (per Month)', digits_compute=dp.get_precision('Product Unit of Measure'), readonly=True),
       'proc_lt_calc': fields.float('Procurement LT (Calculated)', readonly=True),
       'proc_lt_manu': fields.float('Procurement LT (Manual)'),
       'qty_suggested': fields.function(_compute_qty, type='float', string='Suggested Stock Qty', digits_compute=dp.get_precision('Product Unit of Measure'), multi='proc_qty'),
       'qty_variance': fields.function(_compute_qty, type='float', string='Variance', digits_compute=dp.get_precision('Product Unit of Measure'), multi='proc_qty'),
    }
