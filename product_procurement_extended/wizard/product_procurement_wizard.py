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
                ''' to exclude stock moved from 'production' location
                    i.e. consideration for SFG for which both 'out' and 'in' involve 'production' location '''
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
    
    def _compute_proc_lt_calc(self, cr, uid, ids, prod_ids, context=None):
        buy_prod_dict = {}
        produce_prod_list = []
        prod_obj = self.pool.get('product.product')
        bom_obj = self.pool.get('mrp.bom')
        for prod_id in prod_ids:
            prod = prod_obj.browse(cr, uid, [prod_id], context=context)[0]
            if prod.product_tmpl_id.supply_method == 'buy':
                buy_prod_dict[prod.id] = {'type': prod.type, 'lt': 0}
            elif prod.product_tmpl_id.type <> 'service':  # supply_method is 'produce', excluding service items
                produce_prod_list.append(prod.id)
#                 produce_prod_dict[prod.id] = {'seq': produce_seq, 'lt': prod.product_tmpl_id.produce_delay}  # !!!!!
                parent_bom_ids = bom_obj.search(cr, uid, [('product_id','=',prod.id),('bom_id','=',False)])
                if parent_bom_ids:
                    comp_bom_ids = bom_obj.search(cr, uid, [('bom_id','in',parent_bom_ids)])
                    components = bom_obj.browse(cr, uid, comp_bom_ids, context=context)
                    for comp in components:
                        if not comp.product_id.id in prod_ids:
                            prod_ids.append(comp.product_id.id)
#                 produce_seq += 1

        loc_obj = self.pool.get('stock.location')
        # identify internal locations
        int_loc_ids = loc_obj.search(cr, uid, [('usage','=','internal')])
        if len(int_loc_ids) <= 1:
            int_loc_ids.append(999)  # 999 being a dummy loc id
        # identify supplier locations
        supp_loc_ids = loc_obj.search(cr, uid, [('usage','=','supplier')])
        if len(supp_loc_ids) <= 1:
            supp_loc_ids.append(999)  # 999 being a dummy loc id
        # get from_date
        from_date = (datetime.today() + relativedelta(days=-180)).strftime('%Y-%m-%d')
        
        move_obj = self.pool.get('stock.move')
        prodsupp_obj = self.pool.get('product.supplierinfo')
        for k in buy_prod_dict:
            lt_accum = 0
            num_moves = 0
            purch_lt = 0
            if buy_prod_dict[k]['type'] == 'product':
                move_ids = move_obj.search(cr, uid, [('location_id','in',supp_loc_ids),
                    ('location_dest_id','in',int_loc_ids),('product_id','=',k),('state','=','done'),
                    ('date','>=',from_date)])
                if move_ids:
                    for move in move_obj.browse(cr, uid, move_ids, context=context):
                        receipt_date = datetime.strptime(move.date, '%Y-%m-%d %H:%M:%S')
                        order_date = datetime.strptime(move.picking_id.purchase_id.date_order, '%Y-%m-%d')
                        lt_accum += (receipt_date - order_date).days
                        num_moves += 1
                    purch_lt = lt_accum / num_moves
                else:
                    prodsupp_ids = prodsupp_obj.search(cr, uid, [('product_id','=',k)], order='sequence')
                    if prodsupp_ids:
                        purch_lt = prodsupp_obj.browse(cr, uid, prodsupp_ids, context=context)[0].delay
#                         prod_obj.write(cr, uid, k, {'proc_lt_calc': prodsupp_obj.browse(cr, uid, prodsupp_ids, context=context)[0].delay})
#                     else:
#                         prod_obj.write(cr, uid, k, {'proc_lt_calc': 0})
                buy_prod_dict[k]['lt'] = purch_lt
                prod_obj.write(cr, uid, k, {'proc_lt_calc': purch_lt})
#             if buy_prod_dict[k]['type'] == 'service':
                

        prod_list_sorted = []
        for prod_id in produce_prod_list:
            parent_bom_ids = bom_obj.search(cr, uid, [('product_id','=',prod_id),('bom_id','=',False)])
            if parent_bom_ids:
                ok_flag = True
                comp_bom_ids = bom_obj.search(cr, uid, [('bom_id','in',parent_bom_ids)])
                components = bom_obj.browse(cr, uid, comp_bom_ids, context=context)
                for comp in components:
                    if comp.product_id.product_tmpl_id.supply_method == 'produce' \
                        and comp.product_id.product_tmpl_id.id not in prod_list_sorted:
                        ok_flag = False
                        break
                if ok_flag:
                    prod_list_sorted.append(prod_id)
                else:
                    produce_prod_list.append(prod_id)
        
        for produce_prod in prod_obj.browse(cr, uid, prod_list_sorted, context=context):
            manu_lt = produce_prod.produce_delay
            rm_lt = 0  # the longest purchase lead time among comp products
            sfg_lt = 0
            sv_lt = 0
            parent_bom_ids = bom_obj.search(cr, uid, [('product_id','=',produce_prod.id),('bom_id','=',False)])
            if parent_bom_ids:
                comp_bom_ids = bom_obj.search(cr, uid, [('bom_id','in',parent_bom_ids)])
                components = bom_obj.browse(cr, uid, comp_bom_ids, context=context)
                for comp in components:
                    if comp.product_id.product_tmpl_id.type == 'product':
                        if comp.product_id.product_tmpl_id.supply_method == 'buy':
                            if rm_lt < buy_prod_dict[comp.product_id.id]['lt']:
                                rm_lt = buy_prod_dict[comp.product_id.id]['lt']
                        else:  # supply_method is 'produce'
                            if sfg_lt < comp.product_id.proc_lt_calc:
                                sfg_lt = comp.product_id.proc_lt_calc
                    elif comp.product_id.product_tmpl_id.type == 'service':
                        sv_lt += buy_prod_dict[comp.product_id.id]['lt']
            prod_lt = max(rm_lt, sfg_lt)
            prod_obj.write(cr, uid, produce_prod.id, {'proc_lt_calc': manu_lt + prod_lt + sv_lt})
    
    
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
        
        if average_qty:
            for prod in prod_obj.browse(cr, uid, prod_ids, context=context):
                avg_qty_needed = self._compute_avg_qty_needed(cr, uid, ids, prod.id, context=context)
                prod_obj.write(cr, uid, prod.id, {'avg_qty_needed': avg_qty_needed})

        if procure_lt:
            self._compute_proc_lt_calc(cr, uid, ids, prod_ids, context=context)

        return {'type': 'ir.actions.act_window_close'}
