# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _


class pl_report(osv.osv_memory):
    _name = "pl.report"
    _description = "PL Report"

    def onchange_chart_id(self, cr, uid, ids, chart_account_id=False, context=None):
        res = {}
        if chart_account_id:
            company_id = self.pool.get('account.account').browse(cr, uid, chart_account_id, context=context).company_id.id
            now = time.strftime('%Y-%m-%d')
            domain = [('company_id', '=', company_id), ('date_start', '<', now), ('date_stop', '>', now)]
            fiscalyears = self.pool.get('account.fiscalyear').search(cr, uid, domain, limit=1)
            res['value'] = {'company_id': company_id, 'fiscalyear_id': fiscalyears and fiscalyears[0] or False}
        return res

    def onchange_account_report_id(self, cr, uid, ids, account_report_id, context=None):
        if context is None:
            context = {}
        res = {'value': {}}
        
        if account_report_id:
            print "account_report_id=%s"% account_report_id
            res['value'] = {'cmp_type':False,'period_unit':False,'period_unit2':False,
                            'last_year': False, 'two_years_go': False,
                            'date_from':False,'date_to':False}
        return res
    
    def onchange_cmp_type(self, cr, uid, ids, cmp_type=False, context=None):
        if context is None:
            context = {}
        res = {}
        if cmp_type:
            print "cmp_type=%s"% cmp_type
            res['value'] = {'last_year': False, 'two_years_go': False,'date_from':False,'date_to':False}
        return res
    
    def onchange_period_unit(self, cr, uid, ids, period_unit=False, context=None):
        res = {}
        if period_unit:
            res['value'] = {'last_year': False, 'two_years_go': False,'date_from':False,'date_to':False}
        return res
    
    _columns = {
        'chart_account_id': fields.many2one('account.account', 'Chart of Account', required=True, domain = [('parent_id','=',False)]),
        'company_id': fields.related('chart_account_id', 'company_id', type='many2one', relation='res.company', string='Company', readonly=True),
        'cmp_type': fields.selection([('sequential', 'Sequential'),('past_year', 'Past Year'),], 'Comparison type',required=True,),
        'period_unit': fields.selection([('month', 'Month'),('qtr', 'Qtr'),('year', 'Year'),], 'Period Unit'),
        'period_unit2': fields.selection([('month', 'Month'),('qtr', 'Qtr'),], 'Period Unit',),
        'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal Year',required=True, help='Keep empty for all open fiscal year'),
        'account_report_id': fields.many2one('account.financial.report', 'Account Reports', required=True),
        'target_move': fields.selection([('posted', 'All Posted Entries'),('all', 'All Entries'),], 'Target Moves',),
        'last_year': fields.boolean('Last Year', ),
        'two_years_go': fields.boolean('Two Years Ago', ),
        #'date_from': fields.date("Start Date",),
        'date_from': fields.many2one('account.period', 'Start Date',),
        'date_to': fields.many2one('account.period', 'End Date',),
    }

    def _get_account(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        accounts = self.pool.get('account.account').search(cr, uid, [('parent_id', '=', False), ('company_id', '=', user.company_id.id)], limit=1)
        return accounts and accounts[0] or False

    _defaults = {
            'chart_account_id': _get_account,
            'account_report_id': 1,
            'target_move': 'posted',
    }
    
    def _build_month_period(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        result = []
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        period_obj = self.pool.get('account.period')
        if data['form']['cmp_type'] =='sequential':
            if data['form']['period_unit2'] =='month':
                index_start = 1
                if data['form']['date_from']:
                    if data['form']['date_from'] > data['form']['date_to']:
                        raise osv.except_osv(_('Error!'),_("Start Date不能大于End Date，请确认！！"))
                    date_from = period_obj.browse(cr, uid, data['form']['date_from'][0], context=context).date_start
                    index_start = int(date_from[5:7])
                period = period_obj.browse(cr, uid, data['form']['date_to'][0], context=context)
                date_to = period.date_stop
                now = time.strftime('%Y-%m-%d')
                if period.date_start > now:
                    raise osv.except_osv(_('Error!'),_("End Date is later than the current date, please confirm it !"))
                #date_to=2014-08-14
                #month=08
                month = int(date_to[5:7])
                print "date_to=%s"% date_to
                print "month=%s"% month
                for i in range(index_start,month+1):
                    if i >=1 and i <=9:
                        code = '0' + str(i) + '/' + date_to[:4]
                    elif i ==10 or i ==11 or i ==12:
                        code = str(i) + '/' + date_to[:4]
                    period_ids = period_obj.search(cr, uid, [('fiscalyear_id','=',data['form']['fiscalyear_id']),('code','=',code)])
                    period = period_obj.browse(cr, uid, period_ids[0], context=context)
                    date_start = period.date_start or False
                    date_stop = period.date_stop or False
                    ln = {'fiscalyear_id':data['form']['fiscalyear_id'],'date_start':date_start,'date_stop':date_stop,'title':code}
                    result.append(ln)
            elif data['form']['period_unit2'] =='qtr':
                period = period_obj.browse(cr, uid, data['form']['date_to'][0], context=context)
                date_to = period.date_stop
                now = time.strftime('%Y-%m-%d')
                if period.date_start > now:
                    raise osv.except_osv(_('Error!'),_("End Date is later than the current date, please confirm it !"))
                #date_to=2014-08-14
                #month=08
                month = int(date_to[5:7])
                print "date_to=%s"% date_to
                
                if data['form']['date_from']:
                    if data['form']['date_from'] > data['form']['date_to']:
                        raise osv.except_osv(_('Error!'),_("Start Date不能大于End Date，请确认！！"))
                    date_from = period_obj.browse(cr, uid, data['form']['date_from'][0], context=context).date_start
                    index_start = int(date_from[5:7])
                    #计算第一个季度
                    if month == 3:
                        print "month=3"
                        date_start = date_to[:5] + '01-01'
                        date_stop = date_to[:5] + '03-31'
                        title = 'QTR1' + '/' + date_to[:4]
                        ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                        result.append(ln)
                    if month == 6:
                        print "month=6"
                        print "date_from=%s"% date_from
                        if index_start ==1:
                            date_start = date_to[:5] + '01-01'
                            date_stop = date_to[:5] + '03-31'
                            title = 'QTR1' + '/' + date_to[:4]
                            ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                            result.append(ln)
                        date_start = date_to[:5] + '04-01'
                        date_stop = date_to[:5] + '06-30'
                        title = 'QTR2' + '/' + date_to[:4]
                        ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                        result.append(ln)
                    if month == 9:
                        print "month=9"
                        print "date_from=%s"% date_from
                        if index_start ==1:
                            date_start = date_to[:5] + '01-01'
                            date_stop = date_to[:5] + '03-31'
                            title = 'QTR1' + '/' + date_to[:4]
                            ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                            result.append(ln)
                            
                            date_start = date_to[:5] + '04-01'
                            date_stop = date_to[:5] + '06-30'
                            title = 'QTR2' + '/' + date_to[:4]
                            ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                            result.append(ln)
                        if index_start ==4:
                            date_start = date_to[:5] + '04-01'
                            date_stop = date_to[:5] + '06-30'
                            title = 'QTR2' + '/' + date_to[:4]
                            ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                            result.append(ln)
                        date_start = date_to[:5] + '07-01'
                        date_stop = date_to[:5] + '09-30'
                        title = 'QTR3' + '/' + date_to[:4]
                        ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                        result.append(ln)
                    if month == 12:
                        print "month=12"
                        print "date_from=%s"% date_from
                        if index_start ==1:
                            date_start = date_to[:5] + '01-01'
                            date_stop = date_to[:5] + '03-31'
                            title = 'QTR1' + '/' + date_to[:4]
                            ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                            result.append(ln)
                            
                            date_start = date_to[:5] + '04-01'
                            date_stop = date_to[:5] + '06-30'
                            title = 'QTR2' + '/' + date_to[:4]
                            ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                            result.append(ln)
                            
                            date_start = date_to[:5] + '07-01'
                            date_stop = date_to[:5] + '09-30'
                            title = 'QTR3' + '/' + date_to[:4]
                            ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                            result.append(ln)
                            
                        elif index_start ==4:
                            date_start = date_to[:5] + '04-01'
                            date_stop = date_to[:5] + '06-30'
                            title = 'QTR2' + '/' + date_to[:4]
                            ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                            result.append(ln)
                            
                            date_start = date_to[:5] + '07-01'
                            date_stop = date_to[:5] + '09-30'
                            title = 'QTR3' + '/' + date_to[:4]
                            ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                            result.append(ln)
                            
                        elif index_start ==7:
                            date_start = date_to[:5] + '07-01'
                            date_stop = date_to[:5] + '09-30'
                            title = 'QTR3' + '/' + date_to[:4]
                            ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                            result.append(ln)
                            
                        date_start = date_to[:5] + '10-01'
                        date_stop = date_to[:5] + '12-31'
                        title = 'QTR4' + '/' + date_to[:4]
                        ln = {'date_start':date_start,'date_stop':date_stop,'title':title}
                        result.append(ln)
        elif data['form']['cmp_type'] =='past_year':
            if data['form']['period_unit'] =='year':
                fiscalyear_1 = fiscalyear_obj.browse(cr, uid, data['form']['fiscalyear_id'], context=context).name or ''
                ln = {'fiscalyear_id':data['form']['fiscalyear_id'],'title':fiscalyear_1}
                result.append(ln)
                if data['form']['last_year']:
                    fiscalyear_2 = str(int(fiscalyear_1)-1)
                    fiscalyear_ids = fiscalyear_obj.search(cr, uid, [('name','=',fiscalyear_2),])
                    if not fiscalyear_ids:
                        raise osv.except_osv(_('Warning!'),_("FiscalYear %s is not exist !")%(fiscalyear_2))
                    ln = {'fiscalyear_id':fiscalyear_ids[0],'title':fiscalyear_2}
                    result.append(ln)
                if data['form']['two_years_go']:
                    fiscalyear_3 = str(int(fiscalyear_1)-2)
                    fiscalyear_ids = fiscalyear_obj.search(cr, uid, [('name','=',fiscalyear_3),])
                    if not fiscalyear_ids:
                        raise osv.except_osv(_('Warning!'),_("FiscalYear %s is not exist !")%(fiscalyear_3))
                    ln = {'fiscalyear_id':fiscalyear_ids[0],'title':fiscalyear_3}
                    result.append(ln)
            elif data['form']['period_unit'] =='qtr':
                period = period_obj.browse(cr, uid, data['form']['date_to'][0], context=context)
                date_to = period.date_stop
                now = time.strftime('%Y-%m-%d')
                if period.date_start > now:
                    raise osv.except_osv(_('Error!'),_("End Date is later than the current date, please confirm it !"))
                #date_to=2014-03-31
                #month=03
                
                month = date_to[5:7]
                code = month + '/'
                fiscalyear_1 = fiscalyear_obj.browse(cr, uid, data['form']['fiscalyear_id'], context=context).name or ''
                
                if data['form']['date_from'] > data['form']['date_to']:
                    raise osv.except_osv(_('Error!'),_("Start Date不能大于End Date，请确认！！"))
                date_from = period_obj.browse(cr, uid, data['form']['date_from'][0], context=context).date_start
                date_start = date_from
                #title = date_from[5:7] + '/' + fiscalyear_1 + '~' + code + fiscalyear_1
                if int(month) ==3:
                    title = 'QTR1'
                elif int(month) ==6:
                    title = 'QTR2'
                elif int(month) ==9:
                    title = 'QTR3'
                elif int(month) ==12:
                    title = 'QTR4'
                title_1 = title + ' ' + fiscalyear_1
                ln = {'fiscalyear_id':data['form']['fiscalyear_id'],'date_start':date_start,'date_stop':date_to,'title':title_1}
                result.append(ln)
                if data['form']['last_year']:
                    fiscalyear_2 = str(int(fiscalyear_1)-1)
                    code_2 = code + fiscalyear_2
                    print "code_2=%s \n"% code_2
                    fiscalyear_ids = fiscalyear_obj.search(cr, uid, [('name','=',fiscalyear_2),])
                    if not fiscalyear_ids:
                        raise osv.except_osv(_('Warning!'),_("FiscalYear %s is not exist !")%(fiscalyear_2))
                    period_ids = period_obj.search(cr, uid, [('fiscalyear_id','=',fiscalyear_ids[0]),('code','=',code_2)])
                    if not period_ids:
                        raise osv.except_osv(_('Error!'),_("%s年没有%s period请检查！！")%(fiscalyear_2,code_2))
                    period = period_obj.browse(cr, uid, period_ids[0], context=context)
                    date_stop = period.date_stop or False
                    date_start = fiscalyear_2 + date_from[4:]
                    #title = date_from[5:7] + '/' + fiscalyear_2 + '~' + code + fiscalyear_2
                    title_2 = title + ' ' + fiscalyear_2
                    ln = {'fiscalyear_id':fiscalyear_ids[0],'date_start':date_start,'date_stop':date_stop,'title':title_2}
                    result.append(ln)
                if data['form']['two_years_go']:
                    fiscalyear_3 = str(int(fiscalyear_1)-2)
                    code_3 = code  + fiscalyear_3
                    print "code_3=%s"% code_3
                    fiscalyear_ids = fiscalyear_obj.search(cr, uid, [('name','=',fiscalyear_3),])
                    if not fiscalyear_ids:
                        raise osv.except_osv(_('Warning!'),_("FiscalYear %s is not exist !")%(fiscalyear_3))
                    period_ids = period_obj.search(cr, uid, [('fiscalyear_id','=',fiscalyear_ids[0]),('code','=',code_3)])
                    if not period_ids:
                        raise osv.except_osv(_('Error!'),_("%s年没有%s period请检查！！")%(fiscalyear_3,code_3))
                    period = period_obj.browse(cr, uid, period_ids[0], context=context)
                    date_stop = period.date_stop or False
                    date_start = fiscalyear_3 + date_from[4:]
                    #title = date_from[5:7] + '/' + fiscalyear_3 + '~' + code + fiscalyear_3
                    title_3 = title + ' ' + fiscalyear_3
                    ln = {'fiscalyear_id':fiscalyear_ids[0],'date_start':date_start,'date_stop':date_stop,'title':title_3}
                    result.append(ln)
                print "result=%s"% result
                #raise osv.except_osv(_('Error!'),_("End Date 大于当前时间，请确认！！"))
            elif data['form']['period_unit'] =='month':
                period = period_obj.browse(cr, uid, data['form']['date_to'][0], context=context)
                date_to = period.date_stop
                now = time.strftime('%Y-%m-%d')
                if period.date_start > now:
                    raise osv.except_osv(_('Error!'),_("End Date is later than the current date, please confirm it !"))
                #date_to=2014-03-31
                #month=03
                month = date_to[5:7]
                code = month + '/'
                print "date_to=%s "% date_to
                fiscalyear_1 = fiscalyear_obj.browse(cr, uid, data['form']['fiscalyear_id'], context=context).name or ''
                
                if data['form']['date_from'] > data['form']['date_to']:
                    raise osv.except_osv(_('Error!'),_("Start Date不能大于End Date，请确认！！"))
                date_from = period_obj.browse(cr, uid, data['form']['date_from'][0], context=context).date_start
                date_start = date_from
                
                title = date_from[5:7] + '/' + fiscalyear_1 + '~' + code + fiscalyear_1
                ln = {'fiscalyear_id':data['form']['fiscalyear_id'],'date_start':date_start,'date_stop':date_to,'title':title}
                result.append(ln)
                
                if data['form']['last_year']:
                    fiscalyear_2 = str(int(fiscalyear_1)-1)
                    code_2 = code + fiscalyear_2
                    print "code_2=%s \n"% code_2
                    fiscalyear_ids = fiscalyear_obj.search(cr, uid, [('name','=',fiscalyear_2),])
                    if not fiscalyear_ids:
                        raise osv.except_osv(_('Warning!'),_("FiscalYear %s is not exist !")%(fiscalyear_2))
                        
                    period_ids = period_obj.search(cr, uid, [('fiscalyear_id','=',fiscalyear_ids[0]),('code','=',code_2)])
                    if not period_ids:
                        raise osv.except_osv(_('Error!'),_("%s年没有%s period请检查！！")%(fiscalyear_2,code_2))
                    period = period_obj.browse(cr, uid, period_ids[0], context=context)
                    date_stop = period.date_stop or False
                    date_start = fiscalyear_2 + date_from[4:]
                    title = date_from[5:7] + '/' + fiscalyear_2 + '~' + code + fiscalyear_2
                    ln = {'fiscalyear_id':fiscalyear_ids[0],'date_start':date_start,'date_stop':date_stop,'title':title}
                    result.append(ln)
                if data['form']['two_years_go']:
                    fiscalyear_3 = str(int(fiscalyear_1)-2)
                    code_3 = code  + fiscalyear_3
                    print "code_3=%s \n"% code_3
                    fiscalyear_ids = fiscalyear_obj.search(cr, uid, [('name','=',fiscalyear_3),])
                    if not fiscalyear_ids:
                        raise osv.except_osv(_('Warning!'),_("FiscalYear %s is not exist !")%(fiscalyear_3))
                        
                    period_ids = period_obj.search(cr, uid, [('fiscalyear_id','=',fiscalyear_ids[0]),('code','=',code_3)])
                    if not period_ids:
                        raise osv.except_osv(_('Error!'),_("%s年没有%s period请检查！！")%(fiscalyear_3,code_3))
                    period = period_obj.browse(cr, uid, period_ids[0], context=context)
                    date_stop = period.date_stop or False
                    date_start = fiscalyear_3 + date_from[4:]
                    title = date_from[5:7] + '/' + fiscalyear_3 + '~' + code + fiscalyear_3
                    ln = {'fiscalyear_id':fiscalyear_ids[0],'date_start':date_start,'date_stop':date_stop,'title':title}
                    result.append(ln)
        print "result=%s"% result
        #raise osv.except_osv(_('Error!'),_("不再进行下去！！！！"))
        return result

    def check_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        
        res = {}
        data = {}
        month_period = []
        data['form'] = self.read(cr, uid, ids, ['period_unit','period_unit2','cmp_type','chart_account_id','fiscalyear_id','account_report_id','target_move','last_year','two_years_go','date_from','date_to'], context=context)[0]
        data['head'] = {}
        for field in ['chart_account_id','fiscalyear_id','account_report_id']:
            if isinstance(data['form'][field], tuple):
                data['head'][field] = data['form'][field][1]
                data['form'][field] = data['form'][field][0]
        data['head']['cmp_type'] = data['form']['cmp_type']
        data['head']['target_move'] = data['form']['target_move']
        
        print "data1=%s \n"% data
        
        month_period = self._build_month_period(cr, uid, ids, data, context=context)
        #raise osv.except_osv(_('Error!'),_("不再进行下去！！！！"))
        data['month_period'] = month_period
        
        if data['form']['cmp_type'] =='past_year':
            data['head']['period_unit'] = data['form']['period_unit']
            if data['form']['period_unit'] =='year':
                result = {}
                result['fiscalyear'] = 'fiscalyear_id' in data['form'] and data['form']['fiscalyear_id'] or False
                result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
                result['chart_account_id'] = 'chart_account_id' in data['form'] and data['form']['chart_account_id'] or False
                result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
                data['form']['used_context'] = result
                
                res = {
                    'type':'ir.actions.report.xml',
                    'datas':data,
                    'report_name':'bs_pastyear_yr_report',
                }
            elif data['form']['period_unit'] =='qtr' or data['form']['period_unit'] =='month':
                period_obj = self.pool.get('account.period')
                date_to = period_obj.browse(cr, uid, data['form']['date_to'][0], context=context).date_stop
                date_start = period_obj.browse(cr, uid, data['form']['date_from'][0], context=context).date_start
                data['head']['date_from'] = date_start
                data['head']['date_to'] = date_to
                print "data['head']=%s "% data['head']
                #raise osv.except_osv(_('Error!'),_("End Date 大于当前时间，请确认！！"))
                
                result = {}
                result['date_from'] = month_period[0]['date_start']
                result['date_to'] = month_period[0]['date_stop']
                result['fiscalyear'] = 'fiscalyear_id' in data['form'] and data['form']['fiscalyear_id'] or False
                result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
                result['chart_account_id'] = 'chart_account_id' in data['form'] and data['form']['chart_account_id'] or False
                result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
                data['form']['used_context'] = result
                #raise osv.except_osv(_('Error!'),_("不再进行下去！！！！"))
                
                res = {
                    'type':'ir.actions.report.xml',
                    'datas':data,
                    'report_name':'bs_pastyear_month_report',
                }
        elif data['form']['cmp_type'] =='sequential':
            data['head']['period_unit2'] = data['form']['period_unit2']
            period_obj = self.pool.get('account.period')
            date_to = period_obj.browse(cr, uid, data['form']['date_to'][0], context=context).date_stop
            date_start = period_obj.browse(cr, uid, data['form']['date_from'][0], context=context).date_start
            data['head']['date_from'] = date_start
            data['head']['date_to'] = date_to
            print "data['head']=%s "% data['head']
            #raise osv.except_osv(_('Error!'),_("End Date 大于当前时间，请确认！！"))
            
            if data['form']['period_unit2'] =='qtr' or data['form']['period_unit2'] =='month':
                result = {}
                result['date_from'] = month_period[0]['date_start']
                result['date_to'] = month_period[0]['date_stop']
                result['fiscalyear'] = 'fiscalyear_id' in data['form'] and data['form']['fiscalyear_id'] or False
                result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
                result['chart_account_id'] = 'chart_account_id' in data['form'] and data['form']['chart_account_id'] or False
                result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
                data['form']['used_context'] = result
                #raise osv.except_osv(_('Error!'),_("不再进行下去！！！！"))
                
                res = {
                    'type':'ir.actions.report.xml',
                    'datas':data,
                    'report_name':'bs_sequential_month_report',
                }
        return res


pl_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
