# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class account_customer_sales(osv.osv_memory):
    _name = "account.customer.sales"
    _description = "Customer Sales Report"
    _columns = {
        'year_id': fields.many2one('account.fiscalyear','Fiscal Year'),
        'sale_id': fields.many2one('res.users', 'Sales Person'),
        'curr_period': fields.boolean('Include Current Period'),
        'show_top': fields.boolean('Show Top 100', ),
    }

    def _get_fiscalyear(self, cr, uid, context=None):
        return self.pool.get('account.fiscalyear').find(cr, uid, context=context)
    
    _defaults = {
        'year_id': _get_fiscalyear
    }

    def show_sales(self, cr, uid, ids, context=None):
        data = {}
        for params in self.browse(cr, uid, ids, context=context):
            data['year_id'] = params.year_id.id
            data['sale_id'] = params.sale_id.id
            data['curr_period'] = params.curr_period
            data['show_top'] = params.show_top
        return {
            'type':'ir.actions.report.xml',
            'datas':data,
            'report_name':'customer_sales_report',
        }

account_customer_sales()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: