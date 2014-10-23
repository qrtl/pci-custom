# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _

class pl_department(osv.osv_memory):
    _name = "pl.department"
    _description = "PL Department"

    def onchange_chart_id(self, cr, uid, ids, chart_account_id=False, context=None):
        res = {}
        if chart_account_id:
            company_id = self.pool.get('account.account').browse(cr, uid, chart_account_id, context=context).company_id.id
            now = time.strftime('%Y-%m-%d')
            domain = [('company_id', '=', company_id), ('date_start', '<', now), ('date_stop', '>', now)]
            fiscalyears = self.pool.get('account.fiscalyear').search(cr, uid, domain, limit=1)
            res['value'] = {'company_id': company_id, 'fiscalyear_id': fiscalyears and fiscalyears[0] or False}
        return res

    _columns = {
        'chart_account_id': fields.many2one('account.account', 'Chart of Account', required=True, domain = [('parent_id','=',False)]),
        'company_id': fields.related('chart_account_id', 'company_id', type='many2one', relation='res.company', string='Company', readonly=True),
        'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal Year', help='Keep empty for all open fiscal year'),
        'target_move': fields.selection([('posted', 'All Posted Entries'),('all', 'All Entries'),], 'Target Moves',),
        'last_year': fields.boolean('Last Year', ),
        'two_years_go': fields.boolean('Two Years Ago', ),
        'date_from': fields.many2one('account.period', 'Start Period',),
        'date_to': fields.many2one('account.period', 'End Period',),
    }

    def _get_account(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        accounts = self.pool.get('account.account').search(cr, uid, [('parent_id', '=', False), ('company_id', '=', user.company_id.id)], limit=1)
        return accounts and accounts[0] or False

    _defaults = {
            'chart_account_id': _get_account,
            'target_move': 'posted',
    }
    
    def check_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        res = {}
        datas = {}
        res['form'] = self.read(cr, uid, ids, ['chart_account_id','target_move','fiscalyear_id','date_from','date_to'], context=context)[0]
        
        for field in ['date_from','date_to']:
            if isinstance(res['form'][field], tuple):
                res['form'][field] = res['form'][field][0]
        print "res=%s \n"% res
        
        period_obj = self.pool.get('account.period')
        date_from = period_obj.browse(cr, uid, res['form']['date_from'], context=context).date_start or False
        date_to = period_obj.browse(cr, uid, res['form']['date_to'], context=context).date_stop or False
        
        result = {}
        result['date_from'] = date_from
        result['date_to'] = date_to
        result['fiscalyear'] =  'fiscalyear_id' in res['form'] and res['form']['fiscalyear_id'][0] or False
        result['journal_ids'] =  False
        result['chart_account_id'] = 'chart_account_id' in res['form'] and res['form']['chart_account_id'][0] or False
        result['state'] = 'target_move' in res['form'] and res['form']['target_move'] or ''
        print "result=%s \n"% result
        #raise osv.except_osv('Warning !', 'sssssssssss!')
        
        period_obj = self.pool.get('account.period')
        date_from = period_obj.browse(cr,uid,res['form']['date_from']).date_start
        date_to= period_obj.browse(cr,uid,res['form']['date_to']).date_stop
        conditions = [('state','=','valid'),('date','>=',date_from),('date','<=',date_to)]
        am_line_id = self.pool.get('account.move.line').search(cr, uid, conditions)
        #print "am_line_id=%s"% am_line_id
        
        datas={'ids':am_line_id,'used_context': result}
        datas['model'] = 'account.move.line'
        datas['date_from'] = date_from or ''
        datas['date_to'] = date_to or ''
        datas['fiscalyear'] = res['form']['fiscalyear_id'][1] or ''
        datas['chart_account_id'] = res['form']['chart_account_id'][1] or ''
        
        return {
            'type':'ir.actions.report.xml',
            'datas':datas,
            'report_name':'pl_department_report',
        }


pl_department()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
