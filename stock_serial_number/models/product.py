# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class product_category(osv.osv):
    _inherit = "product.category"

    _columns = {
        'enforce_qty_1': fields.boolean('Enforce Qty 1'),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
