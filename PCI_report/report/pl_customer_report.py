# -*- encoding: utf-8 -*-
import time
#from mx.DateTime import *
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


    def printSale(self):
        cr = self.cr
        uid = self.uid

        year_id = self.localcontext.get('year_id', False)
        sale_id = self.localcontext.get('sale_id', False)
        show = self.localcontext.get('show', False)

        # get periods
        period_obj = self.pool.get('account.period')
        period_ids = period_obj.search(cr,uid,[('fiscalyear_id','=',year_id)])
        if period_ids:
            pe_ids = str(tuple(period_ids))

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
        pre_partner = False
        pre_partner1 = False
        line = None 
        total = 0  # sales total of a customer
        period_ids = sorted(period_ids,key = lambda x: x)


        mm = {}  # indicates position?
        i = 1
        for p in period_ids: 
 #           mm[p] = i
            mm[p] = "period" + `i`
            i += 1

#        period = "period"
#        [period+`i` for i in period_ids]

        # get number of effective months
        n = 0  # number of effective months
#                    for i in range(3,14):
#                        if line[i] != 0:
#                            n += 1
#                    if n == 0:
#                        n = 1
#                    if year in years:  # !!!!! what is this?
#                        line[16] = round(total / (monty),2)

        vals = {}
        i = 0
        last_cust = 0
        for ln in sales_data:
            if last_cust != ln['pid']:
                i += 1
                # get country name
                country_id = self.pool.get('res.parnter').browse(cr, uid, ln['pid'])['country_id']
                
                vals[i] = {
                    'cust_name': ln['pnm'],
                    'is_company': str(ln['company']),
                    'cust_id': ln['pid'],
                    #'country': '',
                    'country': '',
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
                    'avg_prev_year': 0,
                    'ratio': 0,
                    }
                last_cust = ln['pid']
            ln['period'] = mm[ln['period']]
            vals[i][ln['period']] += ln['amount']
            vals[i]['total'] += ln['amount']
            lines.append(vals)

            

        lines2 = []
        line2 = None
        if prev_periods:
#            sql2 = """
#            select avl.partner_id as pid, avl.period_id as period, p.name as pnm,p.is_company as company, sum(avl.credit) as amount
#            from account_move_line avl 
#            left join res_partner p on(avl.partner_id = p.id) 
#            left join account_account ac on(avl.account_id =ac.id)
#            where partner_id in %s and period_id in %s and account_id in %s
#            group by avl.partner_id, avl.period_id, p.name, p.is_company
#            order by  avl.partner_id, avl.period_id 
#            """ % (p_ids, prev_periods,a_ids)
            sql2 = """
            select avl.partner_id as pid, avl.period_id as period, p.name as pnm,p.is_company as company, sum(avl.credit) as amount
            from account_move_line avl 
            left join res_partner p on(avl.partner_id = p.id) 
            left join account_account ac on(avl.account_id =ac.id)
            where period_id in %s
            and account_id in %s
            group by avl.partner_id, avl.period_id, p.name, p.is_company
            order by avl.partner_id, avl.period_id 
            """ % (prev_periods, a_ids)
            
            cr.execute(sql2)
            res2 = cr.dictfetchall()
            pre_partner2 = False
            n2 = 0
            total = 0
            for ln in res2:
                if ln["pid"] != pre_partner2:
                    if line2:
                        line2[1] = total / (n2)
                        n2=0
                        lines2.append(line2)
                    line2 = [ln["pid"],0]
                    total = ln["amount"]
                    if ln["amount"]!=0:
                        n2+=1;
                    pre_partner2 = ln["pid"]
                else:
                    if ln["amount"]!=0:
                        n2+=1;
                    total += ln["amount"]
            n2-=1
            if n2==0:
                n2=1
            if total!=0:
                line2[1] = float(total) / float(n2)
            else:
                line2 = [0,0]
            lines2.append(line2)
            lines2=sorted(lines2,key = lambda line: line[1],reverse=True)
            
#        sql1 = """
#            select r.id as pid, c.name as cnm
#            from res_partner r
#            left join res_country c on (r.country_id =c.id)
#            where r.id in %s
#            group by r.id,c.name;
#            """ %(p_ids)
        sql1 = """
            select r.id as pid, c.name as cnm
            from res_partner r
            left join res_country c on (r.country_id =c.id)
            group by r.id,c.name;
            """

        cr.execute(sql1)
        res = cr.dictfetchall()
        pre_partner1 = False
        line = None 
        len_lines = len(lines)
        for ln in res:
            for i in range(len_lines):
                if ln['pid'] == lines[i][2]:
                    lines[i][19] = ln['cnm']
                for ln2 in lines2:
                    if ln2[0] == lines[i][2]:
                        lines[i][17] = round(ln2[1],2)
        lines = sorted(lines,key = lambda line: line[15],reverse=True)

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
