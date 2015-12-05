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
#         rs = report_obj.get_page_count(cr, uid, name, context=context)
#        self.page_cnt = {'min':rs['min'],'first':rs['first'],'mid':rs['mid'],'last':rs['last']}
        self.localcontext.update( {
            'time': time,
            'get_pages':self.get_pages,
        })
        self.context = context

    def get_pages(self,data):
        res = []
        page = {}
        lines = []
        account_obj = self.pool.get('account.account')
        currency_obj = self.pool.get('res.currency')
        report_obj = self.pool.get('account.financial.report')
        ids2 = report_obj._get_children_by_order(self.cr, self.uid, [1], context=data['used_context'])
        
        for report in report_obj.browse(self.cr, self.uid, ids2, context=data['used_context']):
            vals = {
                'name': report.name,
                'balance': report.balance * report.sign or 0.0,
                'type': 'report',
                'level': bool(report.style_overwrite) and report.style_overwrite or report.level,
                'account_type': report.type =='sum' and 'view' or False, #used to underline the financial report balances
            }
            lines.append(vals)

            aa_dict = {}
            aa_obj = self.pool.get('account.analytic.account')
            aa_ids = aa_obj.search(self.cr, self.uid, [('type','!=','view')])
            for aa_rec in aa_obj.browse(self.cr, self.uid, aa_ids):
                aa_dict.update({aa_rec.id: aa_rec.name})
            
            account_ids = []
            if report.display_detail == 'no_detail':
                #the rest of the loop is used to display the details of the financial report, so it's not needed here.
                continue
            if report.type == 'accounts' and report.account_ids:
                account_ids = account_obj._get_children_and_consol(self.cr, self.uid, [x.id for x in report.account_ids])
            elif report.type == 'account_type' and report.account_type_ids:
                account_ids = account_obj.search(self.cr, self.uid, [('user_type','in', [x.id for x in report.account_type_ids])])
            if account_ids:
                for account in account_obj.browse(self.cr, self.uid, account_ids, context=data['used_context']):
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
                    if flag:
                        analytic_account_dic = {}
                        if vals['account_type'] == 'other':
                            acc_id = account_obj.search(self.cr, self.uid, [('code','=',account.code)])[0]
                            for k, v in aa_dict.iteritems():
                                query = 'l.analytic_account_id = ' + `k`
                                aa_bal = account_obj._account_account__compute(self.cr, self.uid, [acc_id], field_names=['balance'], context=data['used_context'], query=query)[acc_id]['balance']
                                if aa_bal:
                                    aa_bal *= report.sign
                                # in case multiple analytic accounts exist with the same name
                                analytic_account_dic[v] = analytic_account_dic.get(v, 0) + aa_bal
                            query = 'l.analytic_account_id is null'
                            aa_bal = account_obj._account_account__compute(self.cr, self.uid, [acc_id], field_names=['balance'], context=data['used_context'], query=query)[acc_id]['balance']
                            if aa_bal:
                                aa_bal *= report.sign
                            analytic_account_dic['Unclassified'] = aa_bal
#                             vals.update({'analytic_account_dic': analytic_account_dic, 'unclassified': aa_bal})
                            vals.update({'analytic_account_dic': analytic_account_dic})
                        lines.append(vals)

        analytic_account = []
        if analytic_account_dic:
            analytic_account = analytic_account_dic.keys()
        
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
        
        page={'no_cmp':True,
              'analytic_account':analytic_account,
              'chart_account_id':data['chart_account_id'],
              'date_from':data['date_from'],
              'date_to':data['date_to'],
              'lines': lines,
              }
              
        res.append(page)
        return res
