# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved.
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
#
##############################################################################

import logging
#import threading
from openerp import pooler, SUPERUSER_ID, tools
from openerp.osv import fields, osv
from datetime import datetime
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class product_proc_info_compute(osv.osv_memory):
    _name = 'product.proc.info.compute'
    _description = 'Compute product procurement info'

    _columns = {
        'average_qty': fields.boolean('Update Average Qty Needed'),
        'procure_lt': fields.boolean('Update Procurement Lead Time'),
    }

    _defaults = {
         'average_qty': lambda *a: False,
         'procure_lt': lambda *a: False,
    }

    def _compute_avg_qty_needed(self, cr, uid, ids, prod_id, context=None):
        res = 0
        loc_obj = self.pool.get('stock.location')
        # identify internal locations
        int_loc_ids = loc_obj.search(cr, uid, [('usage','=','internal')])
        if len(int_loc_ids) == 1:
            loc_param1 = '= '+`int_loc_ids[0]`
        else:
            loc_param1 = 'IN '+`tuple(int_loc_ids)`
 
        from_date = (datetime.today() + relativedelta(days=-180)).strftime('%Y-%m-%d')
 
        prod_obj = self.pool.get('product.product')
        for prod in prod_obj.browse(cr, uid, [prod_id], context=context):
            if prod.product_tmpl_id.supply_method == 'buy':
                virt_loc_ids = loc_obj.search(cr, uid, [('usage','not in',('internal','supplier'))])
                loc_param2 = 'IN '+`tuple(virt_loc_ids)`
                loc_param3 = loc_param2
            else:  # i.e. supply_method is 'produce'
                virt_loc_ids = loc_obj.search(cr, uid, [('usage','!=','internal')])
                loc_param2 = 'IN '+`tuple(virt_loc_ids)`
                # to exclude stock moved from 'production' location
                # i.e. consideration for SFG for which both 'out' and 'in' involve 'production' location
                virt_loc_ids = loc_obj.search(cr, uid, [('usage','not in',('internal','production'))])
                loc_param3 = 'IN '+`tuple(virt_loc_ids)`
 
            for what in ['out', 'in']:
                if what == 'out':
                    params = [loc_param1, loc_param2, prod.id, from_date]
                else:
                    params = [loc_param3, loc_param1, prod.id, from_date]
                sql = """
                    select sum(r.product_qty / u.factor)
                    from stock_move r left join product_uom u on (r.product_uom=u.id)
                    where location_id %s
                    and location_dest_id %s
                    and product_id = %s
                    and state = 'done'
                    and date >= '%s'
                    """ % tuple(params)
                cr.execute(sql)
                if what == 'out':
                    res += cr.dictfetchone()['sum'] or 0
                else:
                    res -= cr.dictfetchone()['sum'] or 0
        return res / 6  # divide by 6 months
    
    def _compute_proc_lt_calc(self, cr, uid, ids, prod_id, context=None):
        return 0
    
    def product_procure_calc(self, cr, uid, ids, context=None):
        for param in self.browse(cr, uid, ids, context=context):
            average_qty = param.average_qty
            procure_lt = param.procure_lt

        prod_ids = []
        prod_obj = self.pool.get('product.product')
        if context.get('active_ids', False):
            prod_ids = context['active_ids']
        else:
            prod_ids = prod_obj.search(cr, uid, [])
        for prod in prod_obj.browse(cr, uid, prod_ids, context=context):
            avg_qty_needed = 0.0
            proc_lt_calc = 0.0

            if average_qty:
                avg_qty_needed = self._compute_avg_qty_needed(cr, uid, ids, prod.id, context=context)
                prod_obj.write(cr, uid, prod.id, {'avg_qty_needed': avg_qty_needed})

            if procure_lt:
                proc_lt_calc = self._compute_proc_lt_calc(cr, uid, ids, prod.id, context=context)
                prod_obj.write(cr, uid, prod.id, {'proc_lt_calc': proc_lt_calc})

        return {'type': 'ir.actions.act_window_close'}
