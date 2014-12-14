# -*- encoding: utf-8 -*-
from datetime import datetime
from datetime import date
import time
from report import report_sxw
import pooler
import logging
import netsvc
import tools
from tools import amount_to_text_en
import logging
import time
_logger = logging.getLogger(__name__)


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        
        self.localcontext.update( {
            'printSale':self.printSale,
            'printSales':self.printSales,
        })

    def set_context(self,objects, data, ids, report_type=None):
        self.localcontext.update({
            'sale_id': data.get('sale_id',False),
            'year_id': data.get('year_id',False),
            'show': data.get('show',False),
        })
        return super(Parser, self).set_context(objects, data, ids, report_type)

    def printSales(self):
        cr = self.cr
        uid = self.uid
        sale_ids = []
        sale_id = self.localcontext.get('sale_id',False)
        if not sale_id:
            sql=""" select user_id from account_invoice GROUP BY user_id"""
            cr.execute(sql)
            users = cr.dictfetchall()
            users = users[1:]
            for res in users:
                if res['user_id']:
                    sale_ids.append(res['user_id'])
        year_id = self.localcontext.get('year_id',False)
        show = self.localcontext.get('show',False)
        account_obj = self.pool.get('account.move.line')
        ac_obj = self.pool.get('account.account')
        period_obj = self.pool.get('account.period')
        partner_obj = self.pool.get('res.partner')
        if sale_id:
            partner_ids=partner_obj.search(cr,uid,[('user_id','=',sale_id)])
        else:
            partner_ids = partner_obj.search(cr,uid,[('user_id','in',sale_ids)])  # !!! this is wrong
        period_ids = period_obj.search(cr,uid,[('fiscalyear_id','=',year_id)])
        ac_ids = ac_obj.search(cr,uid,[('reports','=',True)])
        
        a_ids = ("%s" % ac_ids).replace('[', '(').replace(']', ')')
#        p_ids = ("%s" % partner_ids).replace('[', '(').replace(']', ')')
        pe_ids = ("%s" % period_ids).replace('[', '(').replace(']', ')')
        
        if a_ids == "()":
            a_ids = "(0)"
#        if p_ids == "()":
#            p_ids = "(0)"
        if pe_ids == "()":
            pe_ids = "(0)"
        
        year = self.pool.get('account.fiscalyear').browse(self.cr, self.uid, [year_id])[0].name
        monty = 12
        years = str(time.localtime()[0])
        if year in years:
            monty = time.localtime()[1] or 12
        prev_periods = None
        if year_id - 1 != 0:
            period_ids1 = period_obj.search(cr,uid,[('fiscalyear_id','=',year_id - 1)])
            prev_periods = ("%s" % period_ids1).replace('[', '(').replace(']', ')')
            if prev_periods == "()":
                prev_periods = "(0)"
#        sql = """
#        select ac.name as acname, ml.partner_id as pid, ml.period_id as period, p.name as pnm, p.is_company as company, sum(ml.credit) as amount
#        from account_move_line ml
#        left join res_partner p on (ml.partner_id = p.id)
#        left join account_account ac on (ml.account_id =ac.id)
#        where partner_id in %s
#        and period_id in %s
#        and account_id in %s
#        group by ac.name, ml.partner_id, ml.period_id, p.name, p.is_company
#        order by ml.partner_id, ml.period_id 
#        """ % (p_ids, pe_ids, a_ids)
        sql = """
            select ac.name as acname, ml.partner_id as pid, ml.period_id as period, p.name as pnm, p.is_company as company, sum(ml.credit) as amount
            from account_move_line ml
            left join res_partner p on (ml.partner_id = p.id)
            left join account_account ac on (ml.account_id =ac.id)
            where period_id in %s
            and account_id in %s
            group by ac.name, ml.partner_id, ml.period_id, p.name, p.is_company
            order by ml.partner_id, ml.period_id 
            """ % (pe_ids, a_ids)
        cr.execute(sql)
        res = cr.dictfetchall()
        
        sale_id = self.localcontext.get('sale_id',False)
        year_id = self.localcontext.get('year_id',False)
        ac_obj = self.pool.get('account.account')
        ac_ids = ac_obj.search(cr,uid,[('reports','=',True)])
        accounts = u'Sales Other'
        if ac_ids:
            #accounts=res[0]['acname']
            if res:
                accounts=res[0]['acname']
        name='ALL'
        cr = self.cr
        uid=self.uid
        user_obj = self.pool.get('res.users')
        if sale_id:
            sql=""" select id from res_users where id=%s"""%(sale_id)
            cr.execute(sql)
            user=cr.dictfetchall()
            name=user_obj.browse(cr, uid, user[0]['id']).name
        yesr = self.pool.get('account.fiscalyear').browse(self.cr, self.uid, [year_id])[0].name
        show = self.localcontext.get('show',False)
        if show:
            t='YES'
        else:
            t='NO'
        lines = []
        line = None 
        line = [yesr,name,t,accounts]
        lines.append(line)
        return lines


    def _get_eff_periods(self, cr, uid, year_id, context=None):
        res = 0
#        fiscalyear_obj = self.pool.get('account.fiscalyear')
        today = datetime.today().strftime('%Y-%m-%d')
#        period_obj = self.pool.get('account.period')
        periods = self.pool.get('account.period').search(cr, uid, [('fiscalyear_id','=',year_id),('date_start','<=',today)], count=True)
        res = periods
        return res
    
    def printSale(self):
        cr = self.cr
        uid = self.uid

        year_id = self.localcontext.get('year_id', False)
        sale_id = self.localcontext.get('sale_id', False)
        show = self.localcontext.get('show', False)

        # get periods
        fy_ids = self.pool.get('account.fiscalyear').search(cr, uid, [], order='date_start')
        curr_fy_index = fy_ids.index(year_id)
        prev_fy_id = fy_ids[curr_fy_index - 1]

        period_obj = self.pool.get('account.period')
        period_ids = period_obj.search(cr,uid,['|',('fiscalyear_id','=',year_id),('fiscalyear_id','=',prev_fy_id)])
        if period_ids:
            pe_ids = str(tuple(period_ids))

#        year = self.pool.get('account.fiscalyear').browse(self.cr, self.uid, [year_id])[0].name
#        monty = 12
#        years = str(time.localtime()[0])
#        if year in years:
#            monty = time.localtime()[1] or 12

        #prev_periods = None
        #if year_id - 1 != 0:
        #    period_ids1 = period_obj.search(cr,uid,[('fiscalyear_id','=',year_id - 1)])
        #    prev_periods = ("%s" % period_ids1).replace('[', '(').replace(']', ')')
        #    if prev_periods == "()":
        #        prev_periods = "(0)"

        
        
        # get the periods of the previous FY

        # get sales data
        if not sale_id:
            sql = """
                select ml.partner_id as pid, ml.period_id as period, p.name as pnm, p.is_company as company, sum(ml.credit - ml.debit) as amount
                from account_move_line ml
                left join res_partner p on (ml.partner_id = p.id)
                left join account_account ac on (ml.account_id = ac.id)
                where ml.period_id in %s
                and ac.reports = True
                group by ml.partner_id, ml.period_id, p.name, p.is_company
                order by ml.partner_id, ml.period_id
                """ % (pe_ids)
        else:
            sql = """
                select ml.partner_id as pid, ml.period_id as period, p.name as pnm, p.is_company as company, sum(ml.credit - ml.debit) as amount
                from account_move_line ml
                left join account_invoice inv on (ml.move_id = inv.move_id)
                left join res_partner p on (ml.partner_id = p.id)
                left join account_account ac on (ml.account_id = ac.id)
                where ml.period_id in %s
                and inv.user_id = %s
                and ac.reports = True
                group by ml.partner_id, ml.period_id, p.name, p.is_company
                order by ml.partner_id, ml.period_id
                """ % (pe_ids, sale_id)
            
        cr.execute(sql)
        #res = cr.dictfetchall()
        sales_data = cr.dictfetchall()

        lines = []  # lines for output
#        pre_partner = False
        pre_partner1 = False
        line = None 
        total = 0  # sales total of a customer
        period_ids = sorted(period_ids,key = lambda x: x)


        mm = {}  # mapping between period id and report context
        i = 1
        for period in period_ids: 
            period_fy = self.pool.get('account.period').browse(cr, uid, period).fiscalyear_id.id
            if period_fy == year_id:
                mm[period] = "period" + `i`
                i += 1
            else:
                mm[period] = 'prev_fy'

        # get number of effective months
        eff_periods = self._get_eff_periods(cr, uid, year_id, context=None)

        vals = {}
        i = 0
        last_cust = 0  # a flag to see if the customer has changed
        for ln in sales_data:
            if last_cust != ln['pid']:
                i += 1
                country = self.pool.get('res.partner').browse(cr, uid, ln['pid']).country_id.name  # get country name
                vals[i] = {
                    'cust_name': ln['pnm'],
                    'is_company': str(ln['company']),
                    'cust_id': ln['pid'],
                    'country': country,
                    'period1': 0,
                    'period2': 0,
                    'period3': 0,
                    'period4': 0,
                    'period5': 0,
                    'period6': 0,
                    'period7': 0,
                    'period8': 0,
                    'period9': 0,
                    'period10': 0,
                    'period11': 0,
                    'period12': 0,
                    'total': 0,
                    'avg_curr_year': 0,
                    'prev_period': 0,
                    'avg_prev_year': 0,
                    'ratio': 0,
                    }
                last_cust = ln['pid']
            ln['period'] = mm[ln['period']]
            vals[i][ln['period']] += ln['amount']
            vals[i]['total'] += ln['amount']
            vals[i]['avg_curr_year'] = vals[i]['total'] / eff_periods
            vals[i]['avg_prev_year'] = vals[i]['prev_period'] / 12
            #lines.append(vals)
        # only append values (without key) to form the list
        for k, v in vals.iteritems():
            lines.append(v)

        lines = sorted(lines, key=lambda k: k['total'], reverse=True)

        line = [u'Top 100 Total','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        line1 = [u'Sales Total','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        line2 = [u'Top 100 Ratio','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for lin in lines:
            for i in range(3,18):
                line1[i] += lin[i]
        
        if show:
            if len(lines) >100:
                lines = lines[0:100]
            len_lines = len(lines)
            for lin in lines:
                for i in range(3,18):
                    line[i] += lin[i]
        else:
            m_len = 100
            if len(lines) < 100:
                m_len = len(lines)
            for i in range(m_len):
                for j in range(3,18):
                    line[j] += lines[i][j]

        for i in range(3,17):
            if line1[i] != 0.0:
                line2[i] = str(round(line[i] / line1[i],2)*100) + "%"
            else:
                line2[i] = str(round(line[i],2))+"%"

        lines.append(line)
        lines.append(line1)
        lines.append(line2)
        
        len_line=len(lines)
        for i in range(len_line):
            if lines[i][17] != 0:
                lines[i][18]=str(round(lines[i][16] / lines[i][17],2)*100)+"%"
        return lines
