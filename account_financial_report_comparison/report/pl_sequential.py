# -*- coding: utf-8 -*-
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG
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
#         report_obj = self.pool.get('ir.actions.report.xml')
#         rs = report_obj.get_page_count(cr, uid, name, context=context)
#         self.page_cnt = {'min':rs['min'],'first':rs['first'],'mid':rs['mid'],'last':rs['last']}
        self.localcontext.update({
            'time': time,
            'get_pages': self.get_pages,
        })
        self.context = context
    
    def set_context(self, objects, data, ids, report_type=None):
        new_ids = ids
        if (data['model'] == 'ir.ui.menu'):
            new_ids = 'chart_account_id' in data['form'] and [data['form']['chart_account_id']] or []
            objects = self.pool.get('account.account').browse(self.cr, self.uid, new_ids)
        return super(Parser, self).set_context(objects, data, new_ids, report_type=report_type)

    def _get_cmp_ctx(self, cr, uid, p_param, data_fm):
        res = {}
        res['date_from'] = p_param['date_start']
        res['date_to'] = p_param['date_stop']
        res['fiscalyear'] = p_param['fiscalyear_id']
        res['journal_ids'] = 'journal_ids' in data_fm and data_fm['journal_ids'] or False
        res['chart_account_id'] = 'chart_account_id' in data_fm and data_fm['chart_account_id'] or False
        res['state'] = 'target_move' in data_fm and data_fm['target_move'] or ''
        return res

    def get_pages(self, data):
        res = []
        page = {}
        lines = []
        account_obj = self.pool.get('account.account')
        currency_obj = self.pool.get('res.currency')
        report_obj = self.pool.get('account.financial.report')
        ids2 = report_obj._get_children_by_order(self.cr, self.uid, [data['form']['account_report_id']], context=data['form']['used_context'])

        browse_ctx = data['form']['used_context']
        if data['month_period'][0]['date_start']:
            browse_ctx['date_from'] = data['month_period'][0]['date_start']
        if data['month_period'][0]['date_stop']:
            browse_ctx['date_to'] = data['month_period'][0]['date_stop']
        
#         for report in report_obj.browse(self.cr, self.uid, ids2, context=data['form']['used_context']):
        for report in report_obj.browse(self.cr, self.uid, ids2, context=browse_ctx):
            vals = {
                'name': report.name,
                'balance': report.balance * report.sign or 0.0,
                'type': 'report',
                'level': bool(report.style_overwrite) and report.style_overwrite or report.level,
                'account_type': report.type =='sum' and 'view' or False, #used to underline the financial report balances
                'total': 0.0, 'ave': 0.0, 'total_prev': 0.0, 'ave_prev': 0.0, 'ratio': 0.0,
            }
            if len(data['month_period']) > 1:
                for i in range(1, len(data['month_period'])):
                    cmp_ctx = self._get_cmp_ctx(self.cr, self.uid, data['month_period'][i], data['form'])
                    report_cmp = report_obj.browse(self.cr, self.uid, report.id, context=cmp_ctx)
                    vals['balance_cmp_%s'% i] = report_cmp.balance * report.sign or 0.0
            if data['prev_fy']:
                cmp_ctx = self._get_cmp_ctx(self.cr, self.uid, data['prev_fy'], data['form'])
                report_cmp = report_obj.browse(self.cr, self.uid, report.id, context=cmp_ctx)
                vals['total_prev'] = report_cmp.balance * report.sign or 0.0
            lines.append(vals)
            
            account_ids = []
            if report.display_detail == 'no_detail':
                #the rest of the loop is used to display the details of the financial report, so it's not needed here.
                continue
            if report.type == 'accounts' and report.account_ids:
                account_ids = account_obj._get_children_and_consol(self.cr, self.uid, [x.id for x in report.account_ids])
            elif report.type == 'account_type' and report.account_type_ids:
                account_ids = account_obj.search(self.cr, self.uid, [('user_type','in', [x.id for x in report.account_type_ids])])
            if account_ids:
                for account in account_obj.browse(self.cr, self.uid, account_ids, context=browse_ctx):
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
                        'total': 0.0, 'ave': 0.0, 'total_prev': 0.0, 'ave_prev': 0.0, 'ratio': 0.0,
                    }
                    
                    if not currency_obj.is_zero(self.cr, self.uid, account.company_id.currency_id, vals['balance']):
                        flag = True
                    if len(data['month_period']) > 1:
                        for i in range(1, len(data['month_period'])):
                            cmp_ctx = self._get_cmp_ctx(self.cr, self.uid, data['month_period'][i], data['form'])
                            vals['balance_cmp_%s'% i] = account_obj.browse(self.cr, self.uid, account.id, cmp_ctx).balance * report.sign or 0.0
                            if not currency_obj.is_zero(self.cr, self.uid, account.company_id.currency_id, vals['balance_cmp_%s'% i]):
                                flag = True
                    if data['prev_fy']:
                        cmp_ctx = self._get_cmp_ctx(self.cr, self.uid, data['prev_fy'], data['form'])
                        vals['total_prev'] = account_obj.browse(self.cr, self.uid, account.id, cmp_ctx).balance * report.sign or 0.0
                        if not currency_obj.is_zero(self.cr, self.uid, account.company_id.currency_id, vals['total_prev']):
                            flag = True
                    if flag:
                        lines.append(vals)
        
        num = [k for k in range(len(data['month_period']))]
        for l in lines:
            l.update({'balance_cmp_0': l['balance']})
            total = 0.0
            for x in num:
                total += l['balance_cmp_%s' % x]
            l['total'] = total
            l['ave'] = total / len(num)
            if l['total_prev']:
                if data['form']['period_unit2'] == 'month':
                    l['ave_prev'] = l['total_prev'] / 12
                elif data['form']['period_unit2'] == 'qtr':
                    l['ave_prev'] = l['total_prev'] / 4
                test = l['ave_prev']
                l['ratio'] = l['ave'] / l['ave_prev']
            if l['level']==3:
                l['name'] = '    ' + l['name']
            elif l['level']==4:
                l['name'] = '        ' + l['name']
            elif l['level']==5:
                l['name'] = '            ' + l['name']
            elif l['level']==6:
                l['name'] = '                ' + l['name']
        
        titles =[]
        for p in data['month_period']:
            titles.append(p['title'])
        
        page={'no_cmp':True,'cmp_1':False,
              'chart_account_id': data['head']['chart_account_id'] or '',
              'account_report_id': data['head']['account_report_id'] or '',
              'fiscalyear_id': data['head']['fiscalyear_id'] or '',
              'cmp_type': data['head']['cmp_type'] or '',
              'period_unit2': data['head']['period_unit2'] or '',
              'target_move': data['head']['target_move'] or '',
              'date_from': data['head']['date_from'],
              'date_to': data['head']['date_to'],
              'num': num,
              'titles': titles,
              'lines': lines,
              }
        res.append(page)
        return res
