# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging

class product_product(osv.osv):
    _inherit = "product.product"
    _columns = {
       'avg_qty_needed': fields.float('Average Qty Needed (per Month)'),
       'proc_lt_calc': fields.float('Procurement LT (Calculated)'),
       'proc_lt_manu': fields.float('Procurement LT (Manual)'),
    }
