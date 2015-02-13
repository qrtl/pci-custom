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
from openerp import pooler, SUPERUSER_ID, tools
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
import time
from openerp.osv import fields, osv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import Counter

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
    
    def _get_loc_param(self, cr, uid, ids, usage, context=None):
        loc_obj = self.pool.get('stock.location')
        loc_ids = loc_obj.search(cr, uid, [('usage','in',usage)])
        if loc_ids and len(loc_ids) == 1:
            loc_ids.append(999)  # 999 being a dummy loc id for making through sql
        return tuple(loc_ids)
    
    def _get_prod_ids_param(self, cr, uid, ids, prod_ids, context=None):
        res = prod_ids
        if len(prod_ids) == 1:
            res.append(99999)  # 99999 being a dummy product id to get through sql
        return res
    
    def _get_qty_dict(self, cr, uid, ids, params, context=None):
        res = {}
        sql = """
            select product_id, sum(r.product_qty / u.factor)
            from stock_move r left join product_uom u on (r.product_uom=u.id)
            where location_id IN %s
            and location_dest_id IN %s
            and product_id IN %s
            and state = 'done'
            and date >= '%s'
            group by product_id
            """ % tuple(params)
        cr.execute(sql)
        for d in cr.dictfetchall():
            res[d['product_id']] = d['sum']
        return res
    
    def _get_curr_dict(self, cr, uid, ids, curr_dict_params, context=None):
        res = {}
        sql = """
            select id, %s
            from product_product
            where id IN %s
            """ % tuple(curr_dict_params)
        cr.execute(sql)
        for d in cr.dictfetchall():
            res[d['id']] = d[curr_dict_params[0]]
        return res
    
    def _update_avg_qty_needed(self, cr, uid, ids, prod_ids, from_date, context=None):
        int_loc_param = self._get_loc_param(cr, uid, ids, ['internal'], context=context)
        dest_loc_param = self._get_loc_param(cr, uid, ids, ['customer','production'], context=context)
        return_from_loc_param = self._get_loc_param(cr, uid, ids, ['customer'], context=context)
        prod_ids_param = self._get_prod_ids_param(cr, uid, ids, prod_ids, context=context)
        out_params = [int_loc_param, dest_loc_param, tuple(prod_ids_param), from_date]
        in_params = [return_from_loc_param, int_loc_param, tuple(prod_ids_param), from_date]
        qty_out_dict = self._get_qty_dict(cr, uid, ids, out_params, context=context)
        qty_in_dict = self._get_qty_dict(cr, uid, ids, in_params, context=context)
        qty_dict = dict(Counter(qty_out_dict) - Counter(qty_in_dict))

        curr_dict_params = ['avg_qty_needed', tuple(prod_ids_param)]
        curr_qty_dict = self._get_curr_dict(cr, uid, ids, curr_dict_params, context=context)

        prod_obj = self.pool.get('product.product')
        for prod_id in prod_ids:
            if prod_id in qty_dict:
                if qty_dict[prod_id] / 6 <> curr_qty_dict[prod_id]:
                    prod_obj.write(cr, uid, prod_id, {'avg_qty_needed': qty_dict[prod_id] / 6})  # divide by 6 months
            else:
                if curr_qty_dict[prod_id] <> 0:
                    prod_obj.write(cr, uid, prod_id, {'avg_qty_needed': 0})

    def _get_prodsupp_lt(self, cr, uid, ids, prod, context=None):
        res = 0
        prodsupp_obj = self.pool.get('product.supplierinfo')
        prodsupp_ids = prodsupp_obj.search(cr, uid, [('product_id','=',prod)], order='sequence')
        if prodsupp_ids:
            res = prodsupp_obj.browse(cr, uid, prodsupp_ids, context=context)[0].delay
        return res

    def _get_components(self, cr, uid, ids, domain, context_today, context=None):
        res = []
        bom_obj = self.pool.get('mrp.bom')
        bom_ids = bom_obj.search(cr, uid, domain)
        if bom_ids:
            comp_bom_ids = bom_obj.search(cr, uid, [('bom_id','in',bom_ids),
                '|',('date_start','=',False),('date_start','<=',context_today),
                '|',('date_stop','=',False),('date_stop','>=',context_today)])
            res = bom_obj.browse(cr, uid, comp_bom_ids, context=context)
        return res
    
    def _update_proc_lt_calc(self, cr, uid, ids, prod_ids, from_date, context=None):
        context_today = fields.date.context_today(self, cr, uid, context=context)
        buy_prod_dict = {}
        produce_prod_list = []
        prod_obj = self.pool.get('product.product')
        # prod_ids to capture all the related products by appending bom components
        # then sort products into 'buy' products (buy_prod_dict) and 'produce' products (produce_prod_list)
        for prod in prod_obj.browse(cr, uid, prod_ids, context=context):
            if prod.product_tmpl_id.supply_method == 'buy':
                buy_prod_dict[prod.id] = {'type': prod.type, 'lt': 0}
            elif prod.product_tmpl_id.type <> 'service':  # supply_method is 'produce', excluding service items
                produce_prod_list.append(prod.id)
                components = self._get_components(cr, uid, ids, [('product_id','=',prod.id),('bom_id','=',False)],
                    context_today, context=context)
                for comp in components:
                    if not comp.product_id.id in prod_ids:
                        prod_ids.append(comp.product_id.id)

        # get current proc lt for comparison purpose
        prod_ids_param = self._get_prod_ids_param(cr, uid, ids, prod_ids, context=context)
        curr_dict_params = ['proc_lt_calc', tuple(prod_ids_param)]
        curr_lt_dict = self._get_curr_dict(cr, uid, ids, curr_dict_params, context=context)

        # work on buy_prod_dict and update procurement lead time in db
        loc_obj = self.pool.get('stock.location')
        int_loc_ids = loc_obj.search(cr, uid, [('usage','=','internal')])
        supp_loc_ids = loc_obj.search(cr, uid, [('usage','=','supplier')])
        move_obj = self.pool.get('stock.move')
        inv_ln_obj = self.pool.get('account.invoice.line')
        inv_obj = self.pool.get('account.invoice')
        po_obj = self.pool.get('purchase.order')
        for k in buy_prod_dict:
            inv_ids = []
            lt_accum = 0.0
            num_recs = 0
            purch_lt = 0.0
            if buy_prod_dict[k]['type'] <> 'service':
                move_ids = move_obj.search(cr, uid, [('location_id','in',supp_loc_ids),
                    ('location_dest_id','in',int_loc_ids),('product_id','=',k),('state','=','done'),
                    ('date','>=',from_date)])
                if move_ids:
                    for move in move_obj.browse(cr, uid, move_ids, context=context):
                        receipt_date = datetime.strptime(move.date, '%Y-%m-%d %H:%M:%S')
                        order_date = datetime.strptime(move.picking_id.purchase_id.date_order, DEFAULT_SERVER_DATE_FORMAT)
                        lt_accum += (receipt_date - order_date).days
                        num_recs += 1
            else:  # buy_prod_dict[k]['type'] == 'service':
                inv_ln_ids = inv_ln_obj.search(cr, uid, [('product_id','=',k)])
                if inv_ln_ids:
                    for inv_ln in inv_ln_obj.browse(cr, uid, inv_ln_ids, context=context):
                        if inv_ln.invoice_id.id not in inv_ids:
                            inv_ids.append(inv_ln.invoice_id.id)
                invoice_ids = inv_obj.search(cr, uid, [('id','in',inv_ids),
                    ('state','in',['open','paid']),('type','=','in_invoice'),
                    ('date_invoice','>=',from_date)])
                if invoice_ids:
                    for inv in inv_obj.browse(cr, uid, invoice_ids, context=context):
                        date_invoice = datetime.strptime(inv.date_invoice, DEFAULT_SERVER_DATE_FORMAT)
                        po_ids = po_obj.search(cr, uid, [('name','=',inv.origin)])
                        if po_ids:
                            po = po_obj.browse(cr, uid, po_ids, context=context)[0]
                            order_date = datetime.strptime(po.date_order, DEFAULT_SERVER_DATE_FORMAT)
                            lt_accum += (date_invoice - order_date).days
                            num_recs += 1
            if num_recs:
                purch_lt = lt_accum / num_recs
            else:
                purch_lt = self._get_prodsupp_lt(cr, uid, ids, k, context=context)
            buy_prod_dict[k]['lt'] = purch_lt
            if purch_lt <> curr_lt_dict[k]:
                prod_obj.write(cr, uid, k, {'proc_lt_calc': purch_lt})
            
        # work on produce_prod_list and update procurement lead time in db
        # first sort update prod_list_sorted by sorting produce_prod_list (less dependent products on offsprings first) 
        prod_list_sorted = []
        for prod_id in produce_prod_list:
            ok_flag = True
            components = self._get_components(cr, uid, ids, [('product_id','=',prod_id),('bom_id','=',False)],
                context_today, context=context)
            for comp in components:
                if comp.product_id.product_tmpl_id.supply_method == 'produce' \
                    and comp.product_id.product_tmpl_id.id not in prod_list_sorted:
                    ok_flag = False
                    break
            if ok_flag:
                prod_list_sorted.append(prod_id)
            else:
                produce_prod_list.append(prod_id)  # move the failed product to the end of the list 
        
        for produce_prod in prod_obj.browse(cr, uid, prod_list_sorted, context=context):
            manu_lt = produce_prod.produce_delay
            rm_lt = 0.0  # the longest purchase lead time among comp products
            sfg_lt = 0.0
            sv_lt = 0.0
            produce_prod_lt = 0.0
            components = self._get_components(cr, uid, ids, [('product_id','=',produce_prod.id),('bom_id','=',False)],
                context_today, context=context)
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
            produce_prod_lt = manu_lt + prod_lt + sv_lt
            if produce_prod_lt <> curr_lt_dict[produce_prod.id]:
                prod_obj.write(cr, uid, produce_prod.id, {'proc_lt_calc': produce_prod_lt})
    
    def product_procure_calc(self, cr, uid, ids, context=None):
        for param in self.browse(cr, uid, ids, context=context):
            average_qty = param.average_qty
            procure_lt = param.procure_lt
        prod_ids = []
        prod_obj = self.pool.get('product.product')
        if context.get('active_ids', False):
            prod_ids = context['active_ids']
        else:
            prod_ids = prod_obj.search(cr, uid, [('active','=',True)])
        from_date = (datetime.today() + relativedelta(days=-180)).strftime(DEFAULT_SERVER_DATE_FORMAT)
        
        if average_qty:
            self._update_avg_qty_needed(cr, uid, ids, prod_ids, from_date, context=context)

        if procure_lt:
            self._update_proc_lt_calc(cr, uid, ids, prod_ids, from_date, context=context)

        return {'type': 'ir.actions.act_window_close'}
