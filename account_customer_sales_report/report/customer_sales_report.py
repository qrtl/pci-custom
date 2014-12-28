# -*- encoding: utf-8 -*-
from datetime import datetime
import time
from report import report_sxw
#import pooler
import logging
#import netsvc
#import tools
#from tools import amount_to_text_en
import copy
from collections import Counter
import pytz
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update( {
            'print_sales':self.print_sales,
        })

#     def set_context(self,objects, data, ids, report_type=None):
#         self.localcontext.update({
#             'sale_id': data.get('sale_id',False),
#             'year_id': data.get('year_id',False),
#             'show_top': data.get('show_top',False),
#         })
#         return super(Parser, self).set_context(objects, data, ids, report_type)

    def _get_period_ids(self, cr, uid, year_id, context=None):
        res = []
        fy_ids = self.pool.get('account.fiscalyear').search(cr, uid, [], order='date_start')
        if not fy_ids.index(year_id) == 0:  # to handle the case the selected year is the first year
            prev_fy_id = fy_ids[fy_ids.index(year_id) - 1]
        else:
            prev_fy_id = 0
        res = self.pool.get('account.period').search(cr, uid, ['|',('fiscalyear_id','=',year_id),('fiscalyear_id','=',prev_fy_id),('special','!=',True)], order='date_start')
        return res

    def _get_eff_periods(self, cr, uid, year_id, curr_period, context=None):
        res = 0
        today = datetime.today().strftime('%Y-%m-%d')
        period_obj = self.pool.get('account.period')
        if curr_period:
            res = period_obj.search(cr, uid, [('fiscalyear_id','=',year_id),('date_start','<=',today),('special','!=',True)], count=True)
        else:
            res = period_obj.search(cr, uid, [('fiscalyear_id','=',year_id),('date_stop','<',today),('special','!=',True)], count=True)
        return res

    def _get_header_info(self, cr, uid, year_id, sale_id, show_top, context=None):
        res = []
        # adjust the time according to user's time zone
        user = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid)
        if user.partner_id.tz:
            tz = pytz.timezone(user.partner_id.tz)
        else:
            tz = pytz.utc
        sys_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        report_date = sys_date and pytz.utc.localize(datetime.strptime(sys_date, '%Y-%m-%d %H:%M:%S')).astimezone(tz)
        fy_name = self.pool.get('account.fiscalyear').browse(cr, uid, year_id).name
        if sale_id:
            salesperson = self.pool.get('res.users').browse(cr, uid, sale_id).partner_id.name
        else:
            salesperson = 'ALL'
        header_vals = {
            'report_date': report_date,
            'fy_name': fy_name,
            'salesperson': salesperson,
            'show_top': str(show_top),
            }
        res.append(header_vals)
        return res

    def _get_disp_months(self, cr, uid, year_id, context=None):
        res = []
        period_names = {}
        fy_periods = self.pool.get('account.period').search(cr, uid, [('fiscalyear_id','=',year_id),('special','!=',True)], order='date_start')
        i = 0
        for period in self.pool.get('account.period').browse(cr, uid, fy_periods):
            i += 1
            period_names['p' + `i`] = datetime.strptime(period.date_start, '%Y-%m-%d').strftime('%B')
        res.append(period_names)
        return res

    def _get_sales_data(self, cr, uid, period_ids, curr_period, sale_id, context=None):
        curr_p = self.pool.get('account.period').find(cr, uid, context=context)[0]
        if not curr_period:
            #period_ids.remove(curr_p)
            period_ids = [x for x in period_ids if x != curr_p]
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
                """ % (str(tuple(period_ids)))
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
                """ % (str(tuple(period_ids)), sale_id)
        cr.execute(sql)
        return cr.dictfetchall()

    def _get_lines(self, cr, uid, sales_data, period_ids, year_id, eff_periods, context=None):
        res = []
        line_vals = {}
        map = {}  # mapping between period id and report context
        i = 1
        for p in period_ids:
            period_fy = self.pool.get('account.period').browse(cr, uid, p).fiscalyear_id.id
            if period_fy == year_id:
                map[p] = 'p' + `i`
                i += 1
            else:
                map[p] = 'prev_fy'
        i = 0  # index for aggregated records per customer
        last_cust = 0  # a flag to see if the customer has changed
        for rec in sales_data:
            if last_cust != rec['pid']:
                i += 1
                country = self.pool.get('res.partner').browse(cr, uid, rec['pid']).country_id.name  # get country name
                line_vals[i] = {
                    'name': rec['pnm'],
                    'is_company': str(rec['company']),
                    'cust_id': rec['pid'],
                    'country': country,
                    'p1': 0,
                    'p2': 0,
                    'p3': 0,
                    'p4': 0,
                    'p5': 0,
                    'p6': 0,
                    'p7': 0,
                    'p8': 0,
                    'p9': 0,
                    'p10': 0,
                    'p11': 0,
                    'p12': 0,
                    'total': 0,
                    'avg_curr_year': 0,
                    'prev_fy': 0,
                    'avg_prev_year': 0,
                    'ratio': 0,
                    }
                last_cust = rec['pid']
            rec['period'] = map[rec['period']]
            line_vals[i][rec['period']] += rec['amount']
            if not rec['period'] == 'prev_fy':
                line_vals[i]['total'] += rec['amount']
                line_vals[i]['avg_curr_year'] = line_vals[i]['total'] / eff_periods
            else:
                line_vals[i]['avg_prev_year'] = line_vals[i]['prev_fy'] / 12
                line_vals[i]['ratio'] = line_vals[i]['avg_curr_year'] / line_vals[i]['avg_prev_year']

        # only append values (without key) to form the list
        for k, v in line_vals.iteritems():
            res.append(v)
        res = sorted(res, key=lambda k: k['total'], reverse=True)
        return res
    
    def _get_sumlines(self, cr, uid, lines, context=None):
        res = {
            'totals': [],
            'ratio': [],
            }

        copy_lines = copy.deepcopy(lines)
        c = Counter()
        for d in copy_lines[:100]:  # loop 100 times
            d['name'] = ''
            del d['country']
            del d['is_company']
            d['ratio'] = 0
            c.update(d)
        top_vals = dict(c)
        top_vals['name'] = 'Top-100 Total: '
        if top_vals['prev_fy']:
            top_vals['ratio'] = top_vals['avg_curr_year'] / top_vals['avg_prev_year'] 
        res['totals'].append(top_vals)

        for d in copy_lines[100:]:  # loop from 101th element
            d['name'] = ''
            del d['country']
            del d['is_company']
            d['ratio'] = 0
            c.update(d)
        total_vals = dict(c)
        total_vals['name'] = 'All-Customer Total: '
        if total_vals['prev_fy']:
            total_vals['ratio'] = total_vals['avg_curr_year'] / total_vals['avg_prev_year'] 
        res['totals'].append(total_vals)

        ratio_vals = {
            'name': 'Top-100 Ratio: ',
            'p1': top_vals['p1'] / (total_vals['p1'] or 1),
            'p2': top_vals['p2'] / (total_vals['p2'] or 1),
            'p3': top_vals['p3'] / (total_vals['p3'] or 1),
            'p4': top_vals['p4'] / (total_vals['p4'] or 1),
            'p5': top_vals['p5'] / (total_vals['p5'] or 1),
            'p6': top_vals['p6'] / (total_vals['p6'] or 1),
            'p7': top_vals['p7'] / (total_vals['p7'] or 1),
            'p8': top_vals['p8'] / (total_vals['p8'] or 1),
            'p9': top_vals['p9'] / (total_vals['p9'] or 1),
            'p10': top_vals['p10'] / (total_vals['p10'] or 1),
            'p11': top_vals['p11'] / (total_vals['p11'] or 1),
            'p12': top_vals['p12'] / (total_vals['p12'] or 1),
            'total': top_vals['total'] / (total_vals['total'] or 1),
            'avg_curr_year': top_vals['avg_curr_year'] / (total_vals['avg_curr_year'] or 1),
            'avg_prev_year': top_vals['avg_prev_year'] / (total_vals['avg_prev_year'] or 1),
            }
        ratio_vals['ratio'] = ratio_vals['avg_curr_year'] - ratio_vals['avg_prev_year']
        res['ratio'].append(ratio_vals)
        return res

    def print_sales(self, data):
        res = []
        page = {}
        cr = self.cr
        uid = self.uid
#         year_id = self.localcontext.get('year_id', False)
#         sale_id = self.localcontext.get('sale_id', False)
#         show_top = self.localcontext.get('show_top', False)
        year_id = data['year_id'] or False
        sale_id = data['sale_id'] or False
        curr_period = data['curr_period'] or False
        show_top = data['show_top'] or False
        period_ids = self._get_period_ids(cr, uid, year_id, context=None)
        eff_periods = self._get_eff_periods(cr, uid, year_id, curr_period, context=None)  # get number of effective months

        page['header'] = self._get_header_info(cr, uid, year_id, sale_id, show_top, context=None)
        page['disp_months'] = self._get_disp_months(cr, uid, year_id, context=None)

        sales_data = self._get_sales_data(cr, uid, period_ids, curr_period, sale_id, context=None)
        lines = self._get_lines(cr, uid, sales_data, period_ids, year_id, eff_periods, context=None)
        
        top_lines = []
        if show_top == True:
            for line in lines[:100]:
                top_lines.append(line)
            page['lines'] = top_lines
        else:
            page['lines'] = lines

        sumlines = self._get_sumlines(cr, uid, lines, context=None)
        page['sumlines'] = sumlines['totals']
        page['ratioline'] = sumlines['ratio']
        res.append(page)

        return res
