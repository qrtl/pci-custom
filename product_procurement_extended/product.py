# -*- coding: utf-8 -*-
#    OpenERP, Open Source Management Solution
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
            qty_suggested = avg_qty * proc_lt
            qty_variance = prod.qty_available + prod.incoming_qty - qty_suggested
            res[prod.id] = {
                'qty_suggested': qty_suggested,
                'qty_variance': qty_variance,
                }
        return res

    _columns = {
        'avg_qty_needed': fields.float('Average Qty Needed (per Month)', digits_compute=dp.get_precision('Product Unit of Measure'), readonly=True),
        'avg_qty_adj': fields.float('Adjusted Qty', digits_compute=dp.get_precision('Product Unit of Measure')),
        'avg_qty_adj_comp': fields.float('Average Qty Needed (Adjusted)',
                digits_compute=dp.get_precision('Product Unit of Measure'), readonly=True),
        'proc_lt_calc': fields.float('Procurement LT (Calculated)', readonly=True),
        'proc_lt_manu': fields.float('Procurement LT (Manual)'),
        'qty_suggested': fields.function(_compute_qty, type='float', string='Suggested Stock Qty', digits_compute=dp.get_precision('Product Unit of Measure'), multi='proc_qty'),
        'qty_variance': fields.function(_compute_qty, type='float', string='Variance', digits_compute=dp.get_precision('Product Unit of Measure'), multi='proc_qty'),
    }
