# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import Counter

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT,\
    DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class ProductProcInfoCompute(models.TransientModel):
    _name = 'product.proc.info.compute'
    _description = 'Compute product procurement info'

    average_qty = fields.Boolean(
        'Update Average Qty Needed (Calc)'
    )
    average_qty_adj = fields.Boolean(
        'Update Average Qty Needed (Adjusted)'
    )
    clear_qty_adj = fields.Boolean(
        'Clear "Adjusted Qty" field'
    )
    procure_lt = fields.Boolean(
        'Update Procurement Lead Time'
    )


    def _get_loc_param(self, usage):
        loc_obj = self.env['stock.location']
        locs = loc_obj.search([('usage','in',usage)])
        if len(locs) == 1:
            return '= ' + `locs.id`
        else:
            return 'IN ' + `tuple([l.id for l in locs])`

    def _get_prod_ids_param(self, prod_ids):
        if len(prod_ids) == 1:
            return '= ' + `prod_ids[0]`
        else:
            return 'IN ' + `tuple(prod_ids)`

    def _get_qty_dict(self, params):
        res = {}
        self.env.cr.execute("""
            SELECT
                product_id, SUM(r.product_qty / u.factor)
            FROM
                stock_move r
            LEFT JOIN
                product_uom u on (r.product_uom=u.id)
            WHERE
                location_id %s
                AND location_dest_id %s
                AND product_id %s
                AND state = 'done'
                AND date >= '%s'
            GROUP BY
                product_id
        """ % tuple(params))
        for d in self.env.cr.dictfetchall():
            res[d['product_id']] = d['sum']
        return res

    def _get_bom_prod_ids_sorted(self):
        """
        :return: a sorted list of product ids - those in the upper nodes of BoM
         hierarchy first
        """
        sorted_list = []
        bom_obj = self.env['mrp.bom']
        bom_line_obj = self.env['mrp.bom.line']
        bom_recs = bom_obj.search([('active', '=', True)])
        bom_prod_ids = list(set([b.product_id.id for b in bom_recs]))

        # loop product ids and check if the product id has a bom record in
        # which it is a child.
        # in case the product is a child, it can be appended to sorted_list
        # only when the parent product is already in the list
        for prod_id in bom_prod_ids:
            bom_children = bom_line_obj.search(
                [('product_id', '=', prod_id)]
            )
            if bom_children:
                ok_flag = True
                for child in bom_children:
                    # FIXME handle cases where product template is used
                    parent_prod = bom_obj.browse(child.bom_id.id).product_id.id
                    if parent_prod not in sorted_list:
                        ok_flag = False
                        break
                # if the parent product id is in bom_prod_ids_sorted, the
                # product id should be appended to bom_prod_ids_sorted
                # otherwise, the product id should be put to the end of
                # bom_prod_ids
                if ok_flag == True:
                    sorted_list.append(prod_id)
                else:
                    # prod_id to go back to the end of the list for next try
                    bom_prod_ids.append(prod_id)
            else:
                sorted_list.append(prod_id)
        return sorted_list

    def _get_curr_dict(self, curr_dict_params):
        res = {}
        self.env.cr.execute("""
            SELECT
                id, %s
            FROM
                product_product
            WHERE id %s
        """ % tuple(curr_dict_params))
        for d in self.env.cr.dictfetchall():
            res[d['id']] = d[curr_dict_params[0]]
        return res

    def _update_qty_dict(self, qty_dict, adjust=False):
        # get a sorted list of products used in BoM
        bom_prod_ids_sorted = self._get_bom_prod_ids_sorted()

        # loop through sorted list of BoM components to upate qty_dict,
        # starting from the uppder node of BoM hierarchy (this sequence is
        # important for accurate calculation of required quantities in case
        # multi-level BoM is involved.
        # note that qty_dict gets updated with new elements as the loop
        # proceeds
        for prod_id in bom_prod_ids_sorted:
            if prod_id in qty_dict:
                prod = self.env['product.product'].browse(prod_id)
                boms = self.env['mrp.bom'].search(['product_id', '=', prod.id])
                if boms:
                    for comp in boms.bom_line_ids:
                        if adjust and comp.product_id.avg_qty_adj:
                            continue
                        if comp.product_id.id in qty_dict:
                            qty_dict[comp.product_id.id] += qty_dict[prod_id] * \
                                                            comp.product_qty
                        else:
                            qty_dict[comp.product_id.id] = qty_dict[prod_id] * \
                                                           comp.product_qty
        return qty_dict

    def _update_avg_qty_needed(self, prod_ids, from_date, today, months,
                               adjust=False):
        prod_obj = self.env['product.product']

        # get qty_dict which should first keep shipped quantities to customers
        int_loc_param = self._get_loc_param(['internal'])
        dest_loc_param = self._get_loc_param(['customer'])
        prod_ids_param = self._get_prod_ids_param(prod_ids)
        out_params = [int_loc_param, dest_loc_param, prod_ids_param, from_date]
        in_params = [dest_loc_param, int_loc_param, prod_ids_param, from_date]
        qty_out_dict = self._get_qty_dict(out_params)
        qty_in_dict = self._get_qty_dict(in_params)
        qty_dict = dict(Counter(qty_out_dict) - Counter(qty_in_dict))

        if adjust:
            # get manually input quantities
            qty_manu_dict = {}
            manu_products = prod_obj.search([
                ('id', 'in', prod_ids),
                ('avg_qty_adj', '>', 0)])
            for prod in manu_products:
                qty_manu_dict[prod.id] = prod.avg_qty_adj * months
            # override qty_dict elements with qty_manu_dict
            for prod_id in qty_manu_dict:
                qty_dict[prod_id] = qty_manu_dict[prod_id]
            prod_field = 'avg_qty_adj_comp'
        else:
            prod_field = 'avg_qty_needed'

        # update qty_dict to include component products
        qty_dict = self._update_qty_dict(qty_dict, adjust)

        # get current database values for comparison purpose
        curr_qty_dict = self._get_curr_dict([prod_field, prod_ids_param])

        for prod in prod_obj.browse(prod_ids):
            if prod.id in qty_dict:
                if qty_dict[prod.id] / months <> curr_qty_dict[prod.id]:
                    prod.write({prod_field: qty_dict[prod.id] / months})
            else:
                if curr_qty_dict[prod.id] <> 0:
                    prod.write({prod_field: 0})

    def _get_prodsupp_lt(self, prod):
        res = 0
        prodsupp_obj = self.env['product.supplierinfo']
        prodsupp_recs = prodsupp_obj.search(
            [('product_id', '=', prod)], order='sequence')
        if prodsupp_recs:
            res = prodsupp_recs[0].delay
        return res

    def _update_proc_lt_calc(self, prod_ids, from_date, today):
        buy_prod_dict = {}
        produce_prod_list = []
        prod_obj = self.env['product.product']

        # buy_route: list of 'buy' rountes
        buy_route = self.env['product.template']._get_buy_route()

        # prod_ids to capture all the related products by appending bom
        # components, then sort products into 'buy' products (buy_prod_dict)
        # and 'produce' products (produce_prod_list)
        for prod in prod_obj.browse(prod_ids):
            if buy_route[0] in [prod.product_tmpl_id.route_ids.id]:
                buy_prod_dict[prod.id] = {'type': prod.type, 'lt': 0}
            # FIXME find products using route?
            elif prod.product_tmpl_id.type <> 'service':
                # supply_method is 'produce', excluding service items
                produce_prod_list.append(prod.id)
                bom = self.env['mrp.bom']._bom_find(
                    product=prod, company_id=self.env.user.company_id.id)
                if bom:
                    for comp in bom.bom_line_ids:
                        if not comp.product_id.id in prod_ids:
                            prod_ids.append(comp.product_id.id)

        # get current proc lt for comparison purpose
        prod_ids_param = self._get_prod_ids_param(prod_ids)
        curr_dict_params = ['proc_lt_calc', prod_ids_param]
        curr_lt_dict = self._get_curr_dict(curr_dict_params)

        # work on buy_prod_dict and update procurement lead time in db
        loc_obj = self.env['stock.location']
        int_loc_ids = [l.id for l in loc_obj.search(
            [('usage','=','internal')])]
        supp_loc_ids = [l.id for l in loc_obj.search(
            [('usage','=','supplier')])]
        move_obj = self.env['stock.move']
        inv_ln_obj = self.env['account.invoice.line']
        inv_obj = self.env['account.invoice']
        po_obj = self.env['purchase.order']
        for k in buy_prod_dict:
            inv_ids = []
            lt_accum = 0.0
            num_recs = 0
            if buy_prod_dict[k]['type'] <> 'service':
                moves = move_obj.search(
                    [('location_id', 'in', supp_loc_ids),
                     ('location_dest_id', 'in', int_loc_ids),
                     ('product_id', '=', k),
                     ('state', '=', 'done'),
                     ('date', '>=', from_date)])
                if moves:
                    for move in moves:
                        receipt_date = datetime.strptime(
                            move.date, '%Y-%m-%d %H:%M:%S')
                        if move.picking_id.purchase_id:
                            order_date = datetime.strptime(
                                move.picking_id.purchase_id.date_order,
                                DEFAULT_SERVER_DATETIME_FORMAT)
                            lt_accum += (receipt_date - order_date).days
                            num_recs += 1
            else:  # buy_prod_dict[k]['type'] == 'service':
                inv_lines = inv_ln_obj.search([('product_id', '=', k)])
                if inv_lines:
                    for inv_ln in inv_lines:
                        if inv_ln.invoice_id.id not in inv_ids:
                            inv_ids.append(inv_ln.invoice_id.id)
                invoices = inv_obj.search(
                    [('id', 'in', inv_ids),
                     ('state', 'in', ['open', 'paid']),
                     ('type', '=', 'in_invoice'),
                     ('date_invoice', '>=', from_date)])
                if invoices:
                    for inv in invoices:
                        date_invoice = datetime.strptime(
                            inv.date_invoice, DEFAULT_SERVER_DATE_FORMAT)
                        orders = po_obj.search([('name', '=', inv.origin)])
                        if orders:
                            po = orders[0]
                            order_date = datetime.strptime(
                                po.date_order, DEFAULT_SERVER_DATETIME_FORMAT)
                            lt_accum += (date_invoice - order_date).days
                            num_recs += 1
            if num_recs:
                purch_lt = lt_accum / num_recs / 30
            else:
                purch_lt = self._get_prodsupp_lt(k) / 30
            buy_prod_dict[k]['lt'] = purch_lt
            if purch_lt <> curr_lt_dict[k]:
                prod_obj.browse(k).write({'proc_lt_calc': purch_lt})

        # work on produce_prod_list and update procurement lead time in db
        # first sort update prod_list_sorted by sorting produce_prod_list
        # (less dependent products on offsprings first)
        prod_list_sorted = []
        for prod_id in produce_prod_list:
            ok_flag = True
            prod = self.env['product.product'].browse(prod_id)
            bom = self.env['mrp.bom']._bom_find(
                product=prod, company_id=self.env.user.company_id.id)
            manufacture_route_id = self.env['stock.warehouse'].\
                _get_manufacture_route_id()
            if bom:
                for comp in bom.bom_line_ids:
                    if manufacture_route_id in [
                        comp.product_id.product_tmpl_id.route_ids.id] \
                        and comp.product_id.id not in prod_list_sorted:
                        ok_flag = False
                        break
            if ok_flag:
                prod_list_sorted.append(prod_id)
            else:
                # move the failed product to the end of the list
                produce_prod_list.append(prod_id)

        buy_route = self.env['product.template']._get_buy_route()

        for produce_prod in prod_obj.browse(prod_list_sorted):
            manu_lt = produce_prod.produce_delay
            rm_lt = 0.0  # the longest purchase lead time among comp products
            sfg_lt = 0.0
            sv_lt = 0.0
            bom = self.env['mrp.bom']._bom_find(
                product=produce_prod, company_id=self.env.user.company_id.id)
            if bom:
                for comp in bom.bom_line_ids:
                    if comp.product_id.product_tmpl_id.type == 'product':
                        # FIXME there is no supply_method field
                        # if comp.product_id.product_tmpl_id.supply_method == 'buy':
                        if buy_route[0] in [comp.product_id.product_tmpl_id.route_ids.id]:
                            if rm_lt < buy_prod_dict[comp.product_id.id]['lt']:
                                rm_lt = buy_prod_dict[comp.product_id.id]['lt']
                        else:  # supply_method is 'produce'
                            if sfg_lt < comp.product_id.proc_lt_calc:
                                sfg_lt = comp.product_id.proc_lt_calc
                    elif comp.product_id.product_tmpl_id.type == 'service':
                        sv_lt += buy_prod_dict[comp.product_id.id]['lt']
            prod_lt = max(rm_lt, sfg_lt)
            produce_prod_lt = (manu_lt + prod_lt + sv_lt) / 30
            if produce_prod_lt <> curr_lt_dict[produce_prod.id]:
                produce_prod.proc_lt_calc = produce_prod_lt


    def product_procure_calc(self):
        average_qty = self.average_qty
        average_qty_adj = self.average_qty_adj
        clear_qty_adj = self.clear_qty_adj
        procure_lt = self.procure_lt
        prod_obj = self.env['product.product']
        if self._context.get('active_ids', False):
            prod_ids = self._context['active_ids']
        else:
            prod_ids = [p.id for p in prod_obj.search([('active','=',True)])]
        company_id = self.env.user.company_id.id
        months = self.env['res.company'].browse(company_id).\
            procurement_calc_months
        from_date = (datetime.today() + relativedelta(days=-months*30)).\
            strftime(DEFAULT_SERVER_DATE_FORMAT)
        today = fields.Date.context_today(self)
        if prod_ids and average_qty:
            self._update_avg_qty_needed(
                prod_ids, from_date, today, months, False)
        if prod_ids and average_qty_adj:
            self._update_avg_qty_needed(
                prod_ids, from_date, today, months, True)
        if clear_qty_adj:
            self.env.cr.execute("""
                UPDATE
                    product_product
                SET
                    avg_qty_adj = 0,
                    avg_qty_adj_comp = 0
            """)
        if prod_ids and procure_lt:
            self._update_proc_lt_calc(prod_ids, from_date, today)
        return {'type': 'ir.actions.act_window_close'}
