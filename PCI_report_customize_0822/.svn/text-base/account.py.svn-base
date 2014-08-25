# -*- encoding: utf-8 -*-

from osv import osv, fields
import netsvc
from tools.translate import _
import openerp.addons.decimal_precision as dp
import time


class account_period(osv.osv):
    _inherit = "account.period"
    
    _columns = {
        
    }
    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args=[]
        if not context:
            context={}
        ids = []
        period_ids = []
        if context.get('con_period_unit',False):
            if context['con_period_unit'] =='qtr':
                if context.get('con_fiscalyear_id',False):
                    
                    #period_ids = period_obj.search(cr, uid, [('fiscalyear_id','=',context['con_fiscalyear_id']),('code','=',code)])
                    cr.execute("select id from account_period where fiscalyear_id = %s and (name ilike '%s' or name ilike '%s' or name ilike '%s' or name ilike '%s');"%(context['con_fiscalyear_id'],'03%','06%','09%','12%'))
                    period_ids = [r[0] for r in cr.fetchall()]
                    print "period_ids=%s"%period_ids
                    ids = self.search(cr, uid, [('id','in',period_ids)]+ args, limit=limit, context=context)
                    return self.name_get(cr, uid, ids, context=context)
        if context.get('con_period_unit_start',False):
            if context['con_period_unit_start'] =='qtr':
                if context.get('con_fiscalyear_id',False):
                    
                    #period_ids = period_obj.search(cr, uid, [('fiscalyear_id','=',context['con_fiscalyear_id']),('code','=',code)])
                    cr.execute("select id from account_period where fiscalyear_id = %s and (name ilike '%s' or name ilike '%s' or name ilike '%s' or name ilike '%s');"%(context['con_fiscalyear_id'],'01%','04%','07%','10%'))
                    period_ids = [r[0] for r in cr.fetchall()]
                    print "period_ids=%s"%period_ids
                    ids = self.search(cr, uid, [('id','in',period_ids)]+ args, limit=limit, context=context)
                    return self.name_get(cr, uid, ids, context=context)
                
        return super(account_period, self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)
        
account_period()

