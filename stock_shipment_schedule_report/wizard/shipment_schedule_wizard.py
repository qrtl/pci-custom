# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)


class stock_shipment_schedule(osv.osv_memory):
    _name = "stock.shipment.schedule"
    _description = "Shipment Schedule Report"
    _columns = {
        'threshold_date': fields.date('Threshold Date'),
        'category_id': fields.many2one('product.category', 'Product Category'),
    }

    _defaults = {
        'threshold_date': fields.date.context_today,
    }

    def show_schedule(self, cr, uid, ids, context=None):
        data = {}
        for params in self.browse(cr, uid, ids, context=context):
            data['threshold_date'] = params.threshold_date
            data['category_id'] = params.category_id.id

        return {
            'type':'ir.actions.report.xml',
            'datas':data,
            'report_name':'shipment_schedule_report',
        }

stock_shipment_schedule()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: