# -*- encoding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from report import report_sxw
import pooler
import logging
import tools
import pytz
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update( {
            'print_projection':self.print_projection,
        })

    def set_context(self,objects, data, ids, report_type=None):
        self.localcontext.update({
            'threshold_date': data.get('threshold_date',False),
            'category_id': data.get('category_id',False),
        })
        return super(Parser, self).set_context(objects, data, ids, report_type)

    def _get_user_tz(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid)
        if user.partner_id.tz:
            tz = pytz.timezone(user.partner_id.tz)
        else:
            tz = pytz.utc
        return tz
    
    def _get_current_date(self, cr, uid, tz, context=None):
        sys_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        return pytz.utc.localize(datetime.strptime(sys_date, '%Y-%m-%d %H:%M:%S')).astimezone(tz)
    
    def _get_header_info(self, cr, uid, current_date, threshold_date, category_id, context=None):
        res = []
        if category_id:
            category = self.pool.get('product.category').browse(cr, uid, category_id).name
        else:
            category = 'ALL'
        
        header_vals = {
            'report_date': current_date,
            'threshold_date': threshold_date,
            'category': category,
            }
        res.append(header_vals)
        return res

    def _get_move_qty_data(self, cr, uid, product_ids, periods, line_vals, context=None):
        res = []
        int_loc_ids = self.pool.get('stock.location').search(cr, uid, [('usage','=','internal')])
        i = 0
        for _ in xrange(7):
            date_from = "'"+str(periods[i]['start'])+"'"
            date_to = "'"+str(periods[i]['end'])+"'"
            
            for what in ['in', 'out']:
                if what == 'in':
                    params = ['NOT IN', tuple(int_loc_ids,), 'IN', tuple(int_loc_ids,), tuple(product_ids,), date_from, date_to]
                else:
                    params = ['IN', tuple(int_loc_ids,), 'NOT IN', tuple(int_loc_ids,), tuple(product_ids,), date_from, date_to]
                sql = """
                    select m.product_id, sum(m.product_qty / u.factor)
                    from stock_move m
                    left join product_uom u on (m.product_uom = u.id)
                    where location_id %s %s
                    and location_dest_id %s %s
                    and product_id IN %s
                    and state NOT IN ('done', 'cancel')
                    and m.date_expected >= %s
                    and m.date_expected < %s
                    group by product_id
                    """ % (tuple(params))
                cr.execute(sql)
                data = cr.dictfetchall()
                for rec in data:
                    prod = rec['product_id']
                    line_vals[prod][what+`i`] = rec['sum'] 
            i += 1
        for prod in line_vals:
            i = 2
            for _ in xrange(5):
                line_vals[prod]['bal'+`i`] = line_vals[prod]['bal'+`i-1`] + line_vals[prod]['in'+`i`] - line_vals[prod]['out'+`i`]
                i += 1
        res.append(line_vals)
        return res
  
    def _get_product_ids(self, cr, uid, category_id, context=None):
        categ = self.pool.get('product.category').browse(cr, uid, category_id)
        min = categ.parent_left
        max = categ.parent_right
        prod_obj = self.pool.get('product.product')
        return prod_obj.search(cr, uid, [('sale_ok','=',True),('type','=','product'),('categ_id','>=',min),('categ_id','<=',max)])
 
    def _get_periods(self, cr, uid, current_date_utc, threshold_date_utc, context=None):
        periods = {}
        i = 0
        for _ in xrange(7):
            if i == 0:
                start = current_date_utc - relativedelta(years=100)
                end = current_date_utc
            elif i == 1:
                start = current_date_utc
                end = threshold_date_utc + relativedelta(days=1)
            elif i == 2:
                start = threshold_date_utc - relativedelta(years=100)
                end = threshold_date_utc + relativedelta(days=1) 
            else:
                start = end
                if not i == 6:
                    end = start + relativedelta(days=7)
                else:
                    end += relativedelta(years=100)
            periods[i] = {
                'start': start,
                'end': end,
            }
            i += 1
        return periods
 
    def _get_lines(self, cr, uid, periods, current_date_utc, threshold_date_utc, category_id, context=None):
        res = []
        line_vals = {}
        product_ids = self._get_product_ids(cr, uid, category_id, context=None)
        prod_obj = self.pool.get('product.product')
        #periods = self._get_periods(cr, uid, current_date_utc, threshold_date_utc, context=None)

        for prod in prod_obj.browse(cr, uid, product_ids):
            line_vals[prod.id] = {
                'name': prod.name,
                'categ': prod.categ_id.complete_name,
                'bal1': prod.qty_available,
                'in0': 0.0,
                'out0': 0.0,
                'in1': 0.0,
                'out1': 0.0,
                'in2': 0.0,  # first period in output
                'out2': 0.0,
                'bal2': 0.0,
                'in3': 0.0,  # second period in output
                'out3': 0.0,
                'bal3': 0.0,
                'in4': 0.0,  # third period in output
                'out4': 0.0,
                'bal4': 0.0,
                'in5': 0.0,  # fourth period in output
                'out5': 0.0,
                'bal5': 0.0,
                'in6': 0.0,  # fifth period in output
                'out6': 0.0,
                'bal6': 0.0,
            }
        lines = self._get_move_qty_data(cr, uid, product_ids, periods, line_vals, context=None)

        # only append values (without key) to form the list
        for line in lines:
            for k, v in line.iteritems():
                res.append(v)
        res = sorted(res, key=lambda k: k['categ'])
        return res

    def _get_threshold_date_utc(self, cr, uid, threshold_date, tz, context=None):
        threshold_date = datetime.strptime(threshold_date, '%Y-%m-%d')
        threshold_date_local = tz.localize(threshold_date, is_dst=None)
        return threshold_date_local.astimezone(pytz.utc)

    def _get_line_title(self, cr, uid, periods, tz, context=None):
        line_title = []
        title_vals = {}
        for p in periods:
            if p >= 2:
                if p == 2:
                    start = ''
                else:
                    start =  datetime.strftime(periods[p]['start'].astimezone(tz), '%Y-%m-%d')
                if p == 6:
                    end = ''
                else:
                    end =  datetime.strftime(periods[p]['end'].astimezone(tz) - relativedelta(days=1), '%Y-%m-%d')
                title_vals['p'+`p`] = start + ' ~ ' + end
        line_title.append(title_vals)                
        return line_title

    def print_projection(self, data):
        res = []
        page = {}
        cr = self.cr
        uid = self.uid
        threshold_date = self.localcontext.get('threshold_date', False)
        category_id = self.localcontext.get('category_id', False)

        tz = self._get_user_tz(cr, uid, context=None)
        current_date_local = self._get_current_date(cr, uid, tz, context=None)
        page['header'] = self._get_header_info(cr, uid, current_date_local, threshold_date, category_id, context=None)
        current_date_utc = current_date_local.astimezone(pytz.utc)
        threshold_date_utc = self._get_threshold_date_utc(cr, uid, threshold_date, tz, context=None)
        periods = self._get_periods(cr, uid, current_date_utc, threshold_date_utc, context=None)
        page['line_title'] = self._get_line_title(cr, uid, periods, tz, context=None)
        page['lines'] = self._get_lines(cr, uid, periods, current_date_utc, threshold_date_utc, category_id, context=None)

        res.append(page)

        return res
