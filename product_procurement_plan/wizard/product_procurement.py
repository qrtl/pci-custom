# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import Counter

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT,\
    DEFAULT_SERVER_DATETIME_FORMAT


class ProductProcInfoCompute(models.TransientModel):
    _name = 'product.proc.info.compute'
    _description = 'Compute product procurement info'

    average_qty = fields.Boolean('Update Average Qty Needed (Calc)')
    average_qty_adj = fields.Boolean('Update Average Qty Needed (Adjusted)')
    clear_qty_adj = fields.Boolean('Clear "Adjusted Qty" field')
    procure_lt = fields.Boolean('Update Procurement Lead Time')


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

    def _update_qty_dict(self, qty_dict, sorted_parent_products, adjust=False):
        # loop through sorted list of BoM components to upate qty_dict,
        # starting from the uppder node of BoM hierarchy (this sequence is
        # important for accurate calculation of required quantities in case
        # multi-level BoM is involved.
        # note that qty_dict gets updated with new elements as the loop
        # proceeds
        for prod in sorted_parent_products:
            if prod.id in qty_dict:
                bom = self.env['mrp.bom']._bom_find(
                    product=prod, company_id=self.env.user.company_id.id)
                if bom:
                    for l in bom.bom_line_ids:
                        if adjust and l.product_id.avg_qty_adj:
                            continue
                        if not l.attribute_value_ids or l.attribute_value_ids \
                                in prod.attribute_value_ids:
                            if l.product_id.id in qty_dict:
                                qty_dict[l.product_id.id] += \
                                    qty_dict[prod.id] * l.product_qty
                            else:
                                qty_dict[l.product_id.id] = \
                                    qty_dict[prod.id] * l.product_qty
        return qty_dict

    def _update_avg_qty_needed(self, sorted_parent_products, from_date, months,
                               adjust=False):
        prod_ids = [p.id for p in sorted_parent_products]
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
            manu_products = self.env['product.product'].search([
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
        qty_dict = self._update_qty_dict(qty_dict, sorted_parent_products,
                                         adjust)
        # get current database values for comparison purpose
        curr_qty_dict = self._get_curr_dict([prod_field, prod_ids_param])
        # for prod in sorted_parent_products:
        for prod in self.env['product.product'].browse(list(qty_dict.keys())):
            if prod.id in curr_qty_dict and \
                    qty_dict[prod.id] / months == curr_qty_dict[prod.id]:
                continue
            else:
                prod.write({prod_field: qty_dict[prod.id] / months})

    def _get_prodsupp_lt(self, prod):
        res = 0.0
        prodsupp_obj = self.env['product.supplierinfo']
        prodsupp_recs = prodsupp_obj.search(
            [('product_id', '=', prod)], order='sequence')
        if prodsupp_recs:
            res = prodsupp_recs[0].delay / 30
        return res

    def _get_sorted_products(self, sorted_products):
        buy_prod_dict = {}
        produce_prod_list = []
        buy_route = self.env['product.template']._get_buy_route()  # list
        manufacture_route_id = self.env[
            'stock.warehouse']._get_manufacture_route_id()  # integer
        # prod_ids to capture all the related products by appending bom
        # components, then sort products into 'buy' products (buy_prod_dict)
        # and 'produce' products (produce_prod_list)
        for prod in sorted_products:
            if buy_route[0] in [r.id for r in prod.product_tmpl_id.route_ids]:
                buy_prod_dict[prod.id] = {'type': prod.type, 'lt': 0}
            elif manufacture_route_id in [
                r.id for r in prod.product_tmpl_id.route_ids]:
                produce_prod_list.append(prod)
                bom = self.env['mrp.bom']._bom_find(
                    product=prod, company_id=self.env.user.company_id.id)
                if bom:
                    for comp in bom.bom_line_ids:
                        if not comp.product_id in sorted_products:
                            sorted_products.append(comp.product_id)
        return sorted_products, buy_prod_dict, produce_prod_list

    def _update_prod_proc_lt_calc(self, curr_lt_dict, lt, prod_id):
        if lt != curr_lt_dict[prod_id]:
            self.env['product.product'].browse(prod_id).write(
                {'proc_lt_calc': lt})

    def _update_lt_info_from_moves(self, moves, lt_accum, num_recs):
        for move in moves:
            receipt_date = datetime.strptime(
                move.date, '%Y-%m-%d %H:%M:%S')
            if move.picking_id.purchase_id:
                order_date = datetime.strptime(
                    move.picking_id.purchase_id.date_order,
                    DEFAULT_SERVER_DATETIME_FORMAT)
                lt_accum += (receipt_date - order_date).days
                num_recs += 1
        return lt_accum, num_recs

    def _update_lt_info_from_invoices(self, invoices, lt_accum, num_recs):
        for inv in invoices:
            date_invoice = datetime.strptime(
                inv.date_invoice, DEFAULT_SERVER_DATE_FORMAT)
            orders = self.env['purchase.order'].search(
                [('name', '=', inv.origin)])
            if orders:
                order_date = datetime.strptime(
                    orders[0].date_order,
                    DEFAULT_SERVER_DATETIME_FORMAT
                )
                lt_accum += (date_invoice - order_date).days
                num_recs += 1
        return lt_accum, num_recs

    def _get_invoices(self, prod_id, from_date):
        inv_lines = self.env['account.invoice.line'].search(
            [('product_id', '=', prod_id)])
        if inv_lines:
            inv_ids = list(set(
                [line.invoice_id.id for line in inv_lines]))
            invoices = self.env['account.invoice'].search(
                [('id', 'in', inv_ids),
                 ('state', 'in', ['open', 'paid']),
                 ('type', '=', 'in_invoice'),
                 ('date_invoice', '>=', from_date)])
            if invoices:
                return invoices
        return False

    def _update_buy_prod_procure_lt(
            self, buy_prod_dict, curr_lt_dict, from_date):
        # work on buy_prod_dict and update procurement lead time in db
        loc_obj = self.env['stock.location']
        int_loc_ids = [l.id for l in loc_obj.search(
            [('usage','=','internal')])]
        supp_loc_ids = [l.id for l in loc_obj.search(
            [('usage','=','supplier')])]
        for k in buy_prod_dict:
            lt_accum = 0.0
            num_recs = 0
            if buy_prod_dict[k]['type'] <> 'service':
                moves = self.env['stock.move'].search(
                    [('location_id', 'in', supp_loc_ids),
                     ('location_dest_id', 'in', int_loc_ids),
                     ('product_id', '=', k),
                     ('state', '=', 'done'),
                     ('date', '>=', from_date)])
                if moves:
                    lt_accum, num_recs = self._update_lt_info_from_moves(
                        moves, lt_accum, num_recs)
            else:
                invoices = self._get_invoices(k, from_date)
                if invoices:
                    lt_accum, num_recs = self._update_lt_info_from_invoices(
                        invoices, lt_accum, num_recs)
            if num_recs:
                purch_lt = lt_accum / num_recs / 30
            else:
                purch_lt = self._get_prodsupp_lt(k)
            buy_prod_dict[k]['lt'] = purch_lt
            self._update_prod_proc_lt_calc(curr_lt_dict, purch_lt, k)
        return buy_prod_dict

    def _update_produce_prod_procure_lt(
            self, buy_prod_dict, produce_prod_list, curr_lt_dict):
        manufacture_route_id = self.env['stock.warehouse'].\
            _get_manufacture_route_id()
        buy_route = self.env['product.template']._get_buy_route()
        for produce_prod in produce_prod_list:
            manu_lt = produce_prod.produce_delay / 30
            rm_lt = sfg_lt = sv_lt = 0.0
            bom = self.env['mrp.bom']._bom_find(
                product=produce_prod, company_id=self.env.user.company_id.id)
            if bom:
                for comp in bom.bom_line_ids:
                    if comp.product_id.product_tmpl_id.type != 'service':
                        if buy_route[0] in [
                            comp.product_id.product_tmpl_id.route_ids.ids]:
                            if rm_lt < buy_prod_dict[comp.product_id.id]['lt']:
                                rm_lt = buy_prod_dict[comp.product_id.id]['lt']
                        elif manufacture_route_id in [
                            comp.product_id.product_tmpl_id.route_ids.ids]:
                            if sfg_lt < comp.product_id.proc_lt_calc:
                                sfg_lt = comp.product_id.proc_lt_calc
                    elif comp.product_id.product_tmpl_id.type == 'service':
                        sv_lt += buy_prod_dict[comp.product_id.id]['lt']
            prod_lt = max(rm_lt, sfg_lt)
            produce_prod_lt = manu_lt + prod_lt + sv_lt
            self._update_prod_proc_lt_calc(curr_lt_dict, produce_prod_lt,
                                           produce_prod.id)

    def _update_proc_lt_calc(self, sorted_products, buy_prod_dict,
                             produce_prod_list, from_date):
        # get current proc lt for comparison purpose
        prod_ids = [p.id for p in sorted_products]
        prod_ids_param = self._get_prod_ids_param(prod_ids)
        curr_dict_params = ['proc_lt_calc', prod_ids_param]
        curr_lt_dict = self._get_curr_dict(curr_dict_params)

        buy_prod_dict = self._update_buy_prod_procure_lt(
            buy_prod_dict, curr_lt_dict, from_date)
        self._update_produce_prod_procure_lt(
            buy_prod_dict, produce_prod_list, curr_lt_dict)

    def _get_bom_products(self, products):
        # create a list of bom parent products that are directly related to
        # selected products
        bom_products = []
        bom_obj = self.env['mrp.bom']
        bom_recs = bom_obj.search([('active', '=', True)])
        for rec in bom_recs:
            if rec.product_id and rec.product_id in products and \
                            rec.product_id not in bom_products:
                bom_products.append(rec.product_id)
            if not rec.product_id and rec.product_tmpl_id:
                for prod in rec.product_tmpl_id.product_variant_ids:
                    if prod in products and prod not in bom_products:
                        bom_products.append(prod)
        return bom_products

    def _get_products(self):
        prod_obj = self.env['product.product']
        if self._context.get('active_ids', False):
            prod_ids = self._context['active_ids']
        else:
            prod_ids = [p.id for p in prod_obj.search([('active','=',True)])]
        return prod_obj.browse(prod_ids)

    def _get_sorted_parent_products(self):
        products = self._get_products()
        bom_products = self._get_bom_products(products)
        # loop parent_products and check if the product has a bom record in
        # which it is a child.
        # in case the product is a child,
        # it can be appended to sorted_list
        # only when the parent product is already in the list
        sorted_parent_products = []
        for prod in bom_products:
            bom_lines = self.env['mrp.bom.line'].search(
                [('product_id', '=', prod.id)])
            if bom_lines:
                ok_flag = False
                for l in bom_lines:
                    if l.bom_id.product_id:
                        if l.bom_id.product_id not in sorted_parent_products:
                            break
                    elif not l.bom_id.product_id and l.bom_id.product_tmpl_id:
                        for p in l.bom_id.product_tmpl_id.product_variant_ids:
                            if p in sorted_parent_products:
                                ok_flag = True
                                break
                    else:
                        ok_flag = True
                # if the parent of the product is in sorted_list, the
                # product should be appended to sorted_list
                # otherwise, the product should be put to the end of
                # parent_products for next try
                if ok_flag == True:
                    sorted_parent_products.append(prod)
                else:
                    bom_products.append(prod)
            else:
                sorted_parent_products.append(prod)
        for p in products:
            if p not in sorted_parent_products:
                sorted_parent_products.append(p)
        return sorted_parent_products

    def product_procure_calc(self):
        company_id = self.env.user.company_id.id
        months = self.env['res.company'].browse(company_id).\
            procurement_calc_months
        from_date = (datetime.today() + relativedelta(days=-months*30)).\
            strftime(DEFAULT_SERVER_DATE_FORMAT)
        sorted_parent_products = self._get_sorted_parent_products()
        if sorted_parent_products and self.average_qty:
            self._update_avg_qty_needed(
                sorted_parent_products, from_date, months, False)
        if sorted_parent_products and self.average_qty_adj:
            self._update_avg_qty_needed(
                sorted_parent_products, from_date, months, True)
        if self.clear_qty_adj:
            self.env.cr.execute("""
                UPDATE
                    product_product
                SET
                    avg_qty_adj = 0,
                    avg_qty_adj_comp = 0
            """)
        if sorted_parent_products and self.procure_lt:
            sorted_products, buy_prod_dict, produce_prod_list = \
                self._get_sorted_products(sorted_parent_products)
            self._update_proc_lt_calc(
                sorted_products, buy_prod_dict, produce_prod_list, from_date)
        return {'type': 'ir.actions.act_window_close'}
