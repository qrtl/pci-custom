# -*- encoding: utf-8 -*-

import time
from datetime import datetime
from datetime import timedelta, date
from report import report_sxw
import pooler
import logging
import netsvc
import tools
from openerp.osv import fields, osv
from tools import amount_to_text_en
from tools.translate import _

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        report_obj = self.pool.get('ir.actions.report.xml')
        rs = report_obj.get_page_count(cr, uid, name, context=context)
        self.page_cnt = {'min':rs['min'],'first':rs['first'],'mid':rs['mid'],'last':rs['last']}
        self.localcontext.update( {
            'time': time,
            'get_pages':self.get_pages,
        })
        self.context = context
    
    def set_context(self, objects, data, ids, report_type=None):
        new_ids = ids
        if (data['model'] == 'ir.ui.menu'):
            new_ids = 'chart_account_id' in data['form'] and [data['form']['chart_account_id']] or []
            objects = self.pool.get('account.account').browse(self.cr, self.uid, new_ids)
        return super(Parser, self).set_context(objects, data, new_ids, report_type=report_type)

    def get_pages(self,data):
        res = []
        page = {}
        #print " ddddddddddd data=%s \n"% data
        
        lines = []
        account_obj = self.pool.get('account.account')
        currency_obj = self.pool.get('res.currency')
        report_obj = self.pool.get('account.financial.report')
        ids2 = report_obj._get_children_by_order(self.cr, self.uid, [data['form']['account_report_id']], context=data['form']['used_context'])
        print "ssssssssssssss  ids2=%s"% ids2
        
        for report in report_obj.browse(self.cr, self.uid, ids2, context=data['form']['used_context']):
            print "ssssssssssssss  report=%s"% report
            vals = {
                'name': report.name,
                'balance': report.balance * report.sign or 0.0,
                'type': 'report',
                'level': bool(report.style_overwrite) and report.style_overwrite or report.level,
                'account_type': report.type =='sum' and 'view' or False, #used to underline the financial report balances
            }
            if len(data['month_period'])>1:
                for i in range(1,len(data['month_period'])):
                    cmp_context = {}
                    cmp_context['fiscalyear'] = data['month_period'][i]['fiscalyear_id']
                    cmp_context['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
                    cmp_context['chart_account_id'] = 'chart_account_id' in data['form'] and data['form']['chart_account_id'] or False
                    cmp_context['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
                    
                    report_cmp = report_obj.browse(self.cr, self.uid, report.id, context= cmp_context)
                    vals['balance_cmp_%s'% i] = report_cmp.balance * report.sign or 0.0
                #print "ssssssssssssss  vals=%s"% vals
                #raise osv.except_osv('Warning !', '该报表不是在当前菜单打印!')
            
            lines.append(vals)
            #raise osv.except_osv('Warning !', '该报表不是在当前菜单打印!')
            
            account_ids = []
            if report.display_detail == 'no_detail':
                #the rest of the loop is used to display the details of the financial report, so it's not needed here.
                continue
            if report.type == 'accounts' and report.account_ids:
                account_ids = account_obj._get_children_and_consol(self.cr, self.uid, [x.id for x in report.account_ids])
            elif report.type == 'account_type' and report.account_type_ids:
                account_ids = account_obj.search(self.cr, self.uid, [('user_type','in', [x.id for x in report.account_type_ids])])
            if account_ids:
                
                for account in account_obj.browse(self.cr, self.uid, account_ids, context=data['form']['used_context']):
                    #if there are accounts to display, we add them to the lines with a level equals to their level in
                    #the COA + 1 (to avoid having them with a too low level that would conflicts with the level of data
                    #financial reports for Assets, liabilities...)
                    if report.display_detail == 'detail_flat' and account.type == 'view':
                        continue
                    flag = False
                    vals = {
                        'name': account.code + ' ' + account.name,
                        'balance':  account.balance != 0 and account.balance * report.sign or account.balance,
                        'type': 'account',
                        'level': report.display_detail == 'detail_with_hierarchy' and min(account.level + 1,6) or 6, #account.level + 1
                        'account_type': account.type,
                    }
                    
                    if not currency_obj.is_zero(self.cr, self.uid, account.company_id.currency_id, vals['balance']):
                        flag = True
                    if len(data['month_period'])>1:
                        for i in range(1,len(data['month_period'])):
                            cmp_context = {}
                            cmp_context['fiscalyear'] = data['month_period'][i]['fiscalyear_id']
                            cmp_context['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
                            cmp_context['chart_account_id'] = 'chart_account_id' in data['form'] and data['form']['chart_account_id'] or False
                            cmp_context['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
                            
                            vals['balance_cmp_%s'% i] = account_obj.browse(self.cr, self.uid, account.id, cmp_context).balance * report.sign or 0.0
                            if not currency_obj.is_zero(self.cr, self.uid, account.company_id.currency_id, vals['balance_cmp_%s'% i]):
                                flag = True
                    if flag:
                        lines.append(vals)
        
        for lin in lines:
            
            lin.update({'balance_cmp_0':lin['balance']})
            if lin['level']==3:
                lin['name'] = '    ' + lin['name']
            elif lin['level']==4:
                lin['name'] = '        ' + lin['name']
            elif lin['level']==5:
                lin['name'] = '            ' + lin['name']
            elif lin['level']==6:
                lin['name'] = '                ' + lin['name']
        
        num = [k for k in range(len(data['month_period']))]
        titles =[]
        for ln in data['month_period']:
            titles.append(ln['title'])
        
        #raise osv.except_osv('Warning !', '该报表不是在当前菜单打印!')
        
        page={'no_cmp':True,'cmp_1':False,
              'chart_account_id':data['head']['chart_account_id'] or '',
              'account_report_id':data['head']['account_report_id'] or '',
              'fiscalyear_id':data['head']['fiscalyear_id'] or '',
              'cmp_type':data['head']['cmp_type'] or '',
              'period_unit':data['head']['period_unit'] or '',
              'target_move':data['head']['target_move'] or '',
              'num':num,'titles':titles,'lines':[]}
        print  "page= %s"% page
        page['lines'] = lines
        res.append(page)
        
        return res
