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
            partner_ids = partner_obj.search(cr,uid,[('user_id','in',sale_ids)])  # !!! what is this for?
        period_ids = period_obj.search(cr,uid,[('fiscalyear_id','=',year_id)])
        ac_ids = ac_obj.search(cr,uid,[('reports','=',True)])
        
        a_ids = ("%s" % ac_ids).replace('[', '(').replace(']', ')')
        p_ids = ("%s" % partner_ids).replace('[', '(').replace(']', ')')
        pe_ids = ("%s" % period_ids).replace('[', '(').replace(']', ')')

        
        if a_ids == "()":
            a_ids = "(0)"
        if p_ids == "()":
            p_ids = "(0)"
        if pe_ids == "()":
            pe_ids = "(0)"
        
        year = self.pool.get('account.fiscalyear').browse(self.cr, self.uid, [year_id])[0].name
        monty = 12
        years = str(time.localtime()[0])
        if year in years:
            monty = time.localtime()[1] or 12
        pe_ids1 = None
        if year_id - 1 != 0:
            period_ids1 = period_obj.search(cr,uid,[('fiscalyear_id','=',year_id - 1)])
            pe_ids1 = ("%s" % period_ids1).replace('[', '(').replace(']', ')')
            if pe_ids1 == "()": pe_ids1 = "(0)"
        sql = """
        select ac.name as acname, ml.partner_id as pid, ml.period_id as period, p.name as pnm, p.is_company as company, sum(ml.credit) as amount
        from account_move_line ml
        left join res_partner p on (ml.partner_id = p.id)
        left join account_account ac on (ml.account_id =ac.id)
        where partner_id in %s
        and period_id in %s
        and account_id in %s
        group by ac.name, ml.partner_id, ml.period_id, p.name, p.is_company
        order by ml.partner_id, ml.period_id 
        """ % (p_ids, pe_ids, a_ids)
        cr.execute(sql)
        res = cr.dictfetchall()
        
        sale_id=self.localcontext.get('sale_id',False)
        year_id=self.localcontext.get('year_id',False)
        ac_obj=self.pool.get('account.account')
        ac_ids=ac_obj.search(cr,uid,[('reports','=',True)])
        accounts=u'Sales Other'
        if ac_ids:
            accounts=res[0]['acname']
        name='ALL'
        cr = self.cr
        uid=self.uid
        user_obj=self.pool.get('res.users')
        if sale_id:
            sql=""" select id from res_users where id=%s"""%(sale_id)
            cr.execute(sql)
            user=cr.dictfetchall()
            name=user_obj.browse(cr, uid, user[0]['id']).name
        yesr=self.pool.get('account.fiscalyear').browse(self.cr, self.uid, [year_id])[0].name
        show=self.localcontext.get('show',False)
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
        uid=self.uid
        sale_ids=[]
        sale_id=self.localcontext.get('sale_id',False)
        if not sale_id:
                sql=""" select user_id from account_invoice GROUP BY user_id"""
                cr.execute(sql)
                users=cr.dictfetchall()
                users = users[1:]
                for res in users:
                    if res['user_id']:
                        sale_ids.append(res['user_id'])
        year_id=self.localcontext.get('year_id',False)
        show=self.localcontext.get('show',False)
        account_obj=self.pool.get('account.move.line')
        ac_obj=self.pool.get('account.account')
        period_obj=self.pool.get('account.period')
        partner_obj=self.pool.get('res.partner')
        if sale_id:
            partner_ids=partner_obj.search(cr,uid,[('user_id','=',sale_id)])
        else:
            partner_ids=partner_obj.search(cr,uid,[('user_id','in',sale_ids)])
        period_ids=period_obj.search(cr,uid,[('fiscalyear_id','=',year_id)])
        ac_ids=ac_obj.search(cr,uid,[('reports','=',True)])
        
        a_ids = ("%s" % ac_ids).replace('[', '(').replace(']', ')')
        p_ids = ("%s" % partner_ids).replace('[', '(').replace(']', ')')
        pe_ids = ("%s" % period_ids).replace('[', '(').replace(']', ')')
        
        
        if a_ids == "()": a_ids = "(0)"
        if p_ids == "()": p_ids = "(0)"
        if pe_ids == "()": pe_ids = "(0)"
        
        year=self.pool.get('account.fiscalyear').browse(self.cr, self.uid, [year_id])[0].name
        monty =12
        years=str(time.localtime()[0])
        if year in years:
            monty = time.localtime()[1] or 12
        pe_ids1 = None
        if year_id-1!=0:
            period_ids1=period_obj.search(cr,uid,[('fiscalyear_id','=',year_id-1)])
            pe_ids1 = ("%s" % period_ids1).replace('[', '(').replace(']', ')')
            if pe_ids1 == "()": pe_ids1 = "(0)"
        sql = """
        select avl.partner_id as pid, avl.period_id as period, p.name as pnm,p.is_company as company, sum(avl.credit) as amount from account_move_line avl 
        left join res_partner p on(avl.partner_id = p.id)
        left join account_account ac on(avl.account_id =ac.id)
        where partner_id in %s and period_id in %s and account_id in %s
        group by avl.partner_id, avl.period_id, p.name, p.is_company
        order by  avl.partner_id, avl.period_id 
        """ % (p_ids, pe_ids,a_ids)
        cr.execute(sql)
        res=cr.dictfetchall()
        lines = []
        pre_partner = False
        pre_partner1 = False
        line = None 
        Total = 0
        #["Parnter Name", 3000, 5000, 6000, ...]
        period_ids=sorted(period_ids,key = lambda x: x)
        mm = {}
        i = 3
        for p in period_ids: 
            mm[p]= i
            i += 1
        n=0
        for ln in res:
            if ln["pid"] != pre_partner:
                if line:
                    line[15] = Total
                    for i in range(3,14):
                        if line[i]!=0:
                            n+=1
                    line[15] = round(Total,2)
                    if n==0:
                        n=1
                    line[16] = round(Total / (n),2)
                    n=0
                    lines.append(line)
                if ln['company']:
                    line = [ln["pnm"],'company',ln["pid"],round(ln["amount"],2),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                else:
                    line = [ln["pnm"],'customer',ln["pid"],round(ln["amount"],2),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                Total = ln["amount"]
                pre_partner = ln["pid"]
            else:
                line[mm[ln['period']]] = round(ln["amount"],2)
                Total += ln["amount"]
        if not line: 
            return [["","","","",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
            
        line[16] = Total
        for i in range(3,14):
            if line[i]!=0:
                n+=1
        if n==0:
            n=1
        line[15] = round(Total,2)
        line[16] = round(Total / (n),2)
        if line: 
            lines.append(line)
            
            
        lines2 = []
        line2 = None 
        if pe_ids1:
            sql2 = """
            select avl.partner_id as pid, avl.period_id as period, p.name as pnm,p.is_company as company, sum(avl.credit) as amount from account_move_line avl 
            left join res_partner p on(avl.partner_id = p.id) 
            left join account_account ac on(avl.account_id =ac.id)
            where partner_id in %s and period_id in %s and account_id in %s
            group by avl.partner_id, avl.period_id, p.name, p.is_company
            order by  avl.partner_id, avl.period_id 
            """ % (p_ids, pe_ids1,a_ids)
            
            cr.execute(sql2)
            res2=cr.dictfetchall()
            pre_partner2 = False
            n2=0
            Total=0
            for ln in res2:
                if ln["pid"] != pre_partner2:
                    if line2:
                        line2[1] = Total / (n2)
                        n2=0
                        lines2.append(line2)
                    line2 = [ln["pid"],0]
                    Total = ln["amount"]
                    if ln["amount"]!=0:
                        n2+=1;
                    pre_partner2 = ln["pid"]
                else:
                    if ln["amount"]!=0:
                        n2+=1;
                    Total += ln["amount"]
            n2-=1
            if n2==0:
                n2=1
            if Total!=0:
                line2[1] = float(Total) / float(n2)
            else:
                line2 = [0,0]
            lines2.append(line2)
            lines2=sorted(lines2,key = lambda line: line[1],reverse=True)
            
            
        sql1 = """
        select r.id as pid, c.name as cnm from res_partner r
        left join res_country c on(r.country_id =c.id)
        where r.id in %s
        group by r.id,c.name;
        """ %(p_ids)
        cr.execute(sql1)
        res=cr.dictfetchall()
        pre_partner1 = False
        line = None 
        len_lines=len(lines)
        for ln in res:
            for i in range(len_lines):
                if ln['pid'] == lines[i][2]:
                    lines[i][19]=ln['cnm']
                for ln2 in lines2:
                    if ln2[0] == lines[i][2]:
                        lines[i][17]=round(ln2[1],2)
        lines=sorted(lines,key = lambda line: line[15],reverse=True)
        line = [u'Top100合计','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        line1 = [u'総売り上げ合计','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        line2 = [u'比率','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for lin in lines:
            for i in range(3,18):
                line1[i]+=lin[i]
        
        if show:
            if len(lines) >100:
                lines = lines[0:100]
            len_lines=len(lines)
            for lin in lines:
                for i in range(3,18):
                    line[i] += lin[i]
        else:
            m_len=100
            if len(lines) <100:
                m_len=len(lines)
            for i in range(m_len):
                for j in range(3,18):
                    line[j] += lines[i][j]

        for i in range(3,17):
            if line1[i] != 0.0:
                line2[i]=str(round(line[i] / line1[i],2)*100)+"%"
            else:
                line2[i]=str(round(line[i],2))+"%"
                
        lines.append(line)
        lines.append(line1)
        lines.append(line2)
        
        len_line=len(lines)
        for i in range(len_line):
            if lines[i][17] != 0:
                lines[i][18]=str(round(lines[i][16] / lines[i][17],2)*100)+"%"
        return lines