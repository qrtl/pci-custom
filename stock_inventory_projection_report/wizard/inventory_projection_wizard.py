# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class stock_inventory_projection(osv.osv_memory):
    _name = "stock.inventory.projection"
    _description = "Inventory Projection Report"
    _columns = {
        'threshold_date': fields.date('Threshold Date'),
        'category_id': fields.many2one('product.category', 'Product Category'),
    }

#    def _get_fiscalyear(self, cr, uid, context=None):
#        return self.pool.get('account.fiscalyear').find(cr, uid, context=context)
    
    _defaults = {
#        'year_id': _get_fiscalyear
    }

    def show_projection(self, cr, uid, ids, context=None):
        data = {}
        for params in self.browse(cr, uid, ids, context=context):
            data['threshold_date'] = params.threshold_date
            data['category_id'] = params.category_id.id

        return {
            'type':'ir.actions.report.xml',
            'datas':data,
            'report_name':'inventory_projection_report',
        }

stock_inventory_projection()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: