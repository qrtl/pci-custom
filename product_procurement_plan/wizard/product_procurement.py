# -*- coding: utf-8 -*-
# Copyright 2017-2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.osv import expression


class ProductProcInfoCompute(models.TransientModel):
    _name = "product.proc.info.compute"
    _description = "Compute product procurement info"

    months = fields.Integer(
        "No. of Months for Procurement Calc.",
        default=lambda self: self.env.user.company_id.procurement_calc_months,
        help="Number of months to consider in computation.",
    )
    average_qty = fields.Boolean("Calculate Average Qty", default=True)
    procure_lt = fields.Boolean("Calculate Procurement Lead Time", default=True)

    @api.model
    def _get_products(self):
        product_model = self.env['product.product']
        if self._context.get("active_ids", False):
            product_ids = self._context["active_ids"]
            return product_model.browse(product_ids)

    @api.model
    def _get_bom_line_products(self, products):
        """Returns a recordset of products that are components of effective BOMs,
        amongst the given products.
        """
        bom_products = self.env["mrp.bom"].search(
            [
                "|",
                ("product_id", "in", products.ids),
                ("product_tmpl_id", "in", products.mapped("product_tmpl_id").ids),
            ]
        ).mapped(lambda x: x.product_id or x.product_tmpl_id.product_variant_ids)
        bom_lines = self.env["mrp.bom.line"].search(
            [("product_id", "in", bom_products.ids)]
        )
        # Filter out the lines whose parent products are inactive.
        bom_lines = bom_lines.filtered(
            lambda x: x.bom_id.product_id.active or x.bom_id.product_tmpl_id.active
        )
        return bom_lines.mapped("product_id")

    @api.model
    def _get_sorted_parent_products(self, products):
        """Returns a recordset of products sorted in the order of:
        - top-level products: either the very top of the BOM structure, or products not
          involved in BOM
        - 2nd-level products, 3rd-level products...
        """
        bom_line_products = self._get_bom_line_products(products)
        # Put top-level products in the stack first.
        sorted_parent_products = products - bom_line_products
        # Create a list from the recordset, because otherwise the loop will not consider
        # the elements newly added during the loop.
        bom_line_products = [product for product in bom_line_products]
        # Add lower-level products in the stack according to the BOM structure.
        for product in bom_line_products:
            bom_lines = self.env["mrp.bom.line"].search(
                [("product_id", "=", product.id)]
            )
            if not bom_lines and product not in sorted_parent_products:
                sorted_parent_products += product
            for bom_line in bom_lines:
                parent_products = bom_line.bom_id.mapped(
                    lambda x: x.product_id or x.product_tmpl_id.product_variant_ids
                )
                for parent_product in parent_products:
                    if parent_product in sorted_parent_products:
                        # If the parent is already in the stack, the product is
                        # qualified to be in there as well.
                        sorted_parent_products += product
                        break
                    if parent_product not in bom_line_products:
                        # Add the parent to the end of the looped recordset, so the
                        # parent will eventually be in the stack.
                        bom_line_products += parent_product
            if product not in sorted_parent_products:
                # Add the product to the end of the looped recordset for next try.
                bom_line_products += product
        return sorted_parent_products

    def _get_qty_dict(self, params, months):
        res = {}
        self.env.cr.execute("""
            SELECT
                product_id, SUM(r.product_qty / u.factor)
            FROM
                stock_move r
            LEFT JOIN
                product_uom u ON (r.product_uom=u.id)
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
            res[d["product_id"]] = d["sum"] / months
        return res

    @api.model
    def _update_qty_dict(self, qty_dict, sorted_parent_products, adjust=False):
        """Loop through sorted list of BoM components to upate qty_dict, starting from
        the uppder node of BoM hierarchy (this sequence is important for accurate
        calculation of required quantities in case multi-level BoM is involved.
        Note that qty_dict gets updated with new elements as the loop proceeds
        """
        for prod in sorted_parent_products:
            if prod.id not in qty_dict:
                continue
            bom = self.env["mrp.bom"]._bom_find(product=prod)
            for line in bom.bom_line_ids:
                if adjust and line.product_id.avg_qty_man:
                    continue
                if not line.attribute_value_ids or line.attribute_value_ids \
                        in prod.attribute_value_ids:
                    qty_dict.setdefault(line.product_id.id, 0.0)
                    qty_dict[line.product_id.id] += qty_dict[prod.id] * line.product_qty
        return qty_dict

    @api.model
    def _get_location_param(self, usage):
        locations = self.env['stock.location'].search([("usage", "=", usage)])
        if len(locations) == 1:
            return "= %s" % locations.id
        return "IN %s" % (tuple(locations.ids),)

    @api.model
    def _get_product_param(self, product_ids):
        if len(product_ids) == 1:
            return "= %s" % product_ids[0]
        return "IN %s" % (tuple(product_ids),)

    @api.model
    def _get_qty_dict_params(self, products, from_date):
        int_loc_param = self._get_location_param("internal")
        dest_loc_param = self._get_location_param("customer")
        product_param = self._get_product_param(products.ids)
        out_params = [int_loc_param, dest_loc_param, product_param, from_date]
        in_params = [dest_loc_param, int_loc_param, product_param, from_date]
        return out_params, in_params

    @api.model
    def _update_avg_qty(self, sorted_products, from_date, months):
        # Get qty_dict which should first keep shipped quantities to customers
        qty_dict = {id: 0 for id in sorted_products.ids}  # Initialize
        out_params, in_params = self._get_qty_dict_params(sorted_products, from_date)
        for product_id, qty in self._get_qty_dict(out_params, months).items():
            qty_dict[product_id] += qty
        for product_id, qty in self._get_qty_dict(in_params, months).items():
            qty_dict[product_id] -= qty
        # Update qty_dict to include component products
        qty_dict = self._update_qty_dict(qty_dict, sorted_products, adjust=False)
        for product in self.env["product.product"].browse(qty_dict.keys()):
            avg_qty = qty_dict[product.id]
            product.write({"avg_qty_calc": avg_qty, "avg_qty_adj": avg_qty})

    @api.model
    def _update_avg_qty_adj(self, sorted_products):
        qty_dict = {}
        for product in sorted_products:
            # Use the computed qty if adjusted qty is not available.
            qty_dict[product.id] = product.avg_qty_man or product.avg_qty_calc
        # Update qty_dict to include component products
        qty_dict = self._update_qty_dict(qty_dict, sorted_products, adjust=True)
        for product in self.env["product.product"].browse(qty_dict.keys()):
            avg_qty = qty_dict[product.id]
            product.write({"avg_qty_adj": avg_qty})

    @api.model
    def _get_leadtime_data(self, sorted_products):
        buy_prod_dict = {}
        produce_products = self.env["product.product"]
        buy_route = self.env["product.template"]._get_buy_route()  # list
        manufacture_route_id = self.env["stock.warehouse"]._get_manufacture_route_id()
        # Create a list from the recordset, because otherwise the loop will not consider
        # the elements newly added during the loop.
        sorted_products = [product for product in sorted_products]
        # prod_ids to capture all the related products by appending bom
        # components, then sort products into 'buy' products (buy_prod_dict)
        # and 'produce' products (produce_products)
        for product in sorted_products:
            if buy_route[0] in [r.id for r in product.route_ids]:
                buy_prod_dict[product] = 0
            elif manufacture_route_id in [r.id for r in product.route_ids]:
                produce_products += product
                bom = self.env["mrp.bom"]._bom_find(product=product)
                for line in bom.bom_line_ids:
                    if line.product_id not in sorted_products:
                        sorted_products.append(line.product_id)
        return buy_prod_dict, produce_products

    @api.model
    def _get_move_domain(self, from_date):
        location_model = self.env['stock.location']
        supplier_locations = location_model.search([("usage", "=", "supplier")])
        internal_locations = location_model.search([("usage", "=", "internal")])
        return [
            ("location_id", "in", supplier_locations.ids),
            ("location_dest_id", "in", internal_locations.ids),
            ("state", "=", "done"),
            ("date", ">=", from_date),
        ]

    @api.model
    def _update_lt_info_from_moves(self, moves, lt_accum, num_recs):
        for move in moves:
            receipt_date = datetime.strptime(move.date, DATETIME_FORMAT)
            if move.picking_id.purchase_id:
                order_date = datetime.strptime(
                    move.picking_id.purchase_id.date_order, DATETIME_FORMAT
                )
                lt_accum += (receipt_date - order_date).days
                num_recs += 1
        return lt_accum, num_recs

    @api.model
    def _update_lt_info_from_invoice_lines(self, invoice_lines, lt_accum, num_recs):
        for line in invoice_lines:
            date_invoice = datetime.strptime(
                line.invoice_id.date_invoice, DATE_FORMAT
            )
            order_date = datetime.strptime(
                line.purchase_line_id.order_id.date_order, DATETIME_FORMAT
            )
            lt_accum += (date_invoice - order_date).days
            num_recs += 1
        return lt_accum, num_recs

    @api.model
    def _update_buy_prod_procure_lt(self, buy_prod_dict, from_date):
        """Update procurement lead time of purchased products.
        Returns buy_prod_dict with updated lead time.
        """
        domain = self._get_move_domain(from_date)
        for product in buy_prod_dict:
            lt_accum = 0.0
            num_recs = 0
            if product.type == "service":
                invoice_lines = self.env["account.invoice.line"].search([
                    ("product_id", "=", product.id),
                    ("purchase_line_id", "!=", False)
                ]).filtered(
                    lambda x: x.invoice_id.state in ("open", "paid")
                    and x.invoice_id.date_invoice >= from_date
                )
                lt_accum, num_recs = self._update_lt_info_from_invoice_lines(
                    invoice_lines, lt_accum, num_recs
                )
            else:
                move_domain = expression.AND(
                    [domain, [("product_id", "=", product.id)]]
                )
                moves = self.env["stock.move"].search(move_domain)
                lt_accum, num_recs = self._update_lt_info_from_moves(
                    moves, lt_accum, num_recs
                )
            if num_recs:
                purch_lt = lt_accum / num_recs / 30
            else:
                purch_lt = product._select_seller(quantity=1.0).delay / 30
            buy_prod_dict[product] = purch_lt
            if purch_lt != product.proc_lt_calc:
                product.write({"proc_lt_calc": purch_lt})
        return buy_prod_dict

    @api.model
    def _update_produce_prod_procure_lt(self, buy_prod_dict, produce_products):
        manufacture_route_id = self.env["stock.warehouse"]._get_manufacture_route_id()
        buy_route = self.env["product.template"]._get_buy_route()
        for produce_prod in produce_products:
            manu_lt = produce_prod.produce_delay / 30
            rm_lt = sfg_lt = sv_lt = 0.0
            bom = self.env["mrp.bom"]._bom_find(product=produce_prod)
            for line in bom.bom_line_ids:
                product = line.product_id
                if line.product_id.type == "service":
                    sv_lt += buy_prod_dict[product]
                elif buy_route[0] in product.route_ids.ids:
                    rm_lt = max(rm_lt, buy_prod_dict[product])
                elif manufacture_route_id in product.route_ids.ids:
                    sfg_lt = max(sfg_lt, product.proc_lt_calc)
            prod_lt = max(rm_lt, sfg_lt)
            produce_prod_lt = manu_lt + prod_lt + sv_lt
            if produce_prod_lt != produce_prod.proc_lt_calc:
                produce_prod.write({"proc_lt_calc": produce_prod_lt})

    @api.multi
    def product_procure_calc(self):
        self.ensure_one()
        from_date = (datetime.today() - relativedelta(days=self.months*30)).\
            strftime(DATE_FORMAT)
        selected_products = self._get_products()
        sorted_products = self._get_sorted_parent_products(selected_products)
        if not sorted_products:
            return {"type": "ir.actions.act_window_close"}
        if self.average_qty:
            # Update Avg Qty (Calc) and Avg Qty (Adj)
            self._update_avg_qty(sorted_products, from_date, self.months)
            man_adj_products = sorted_products.filtered(lambda x: x.avg_qty_man > 0)
            sorted_adj_products = self._get_sorted_parent_products(man_adj_products)
            if sorted_adj_products:
                # Update Avg Qty (Adj) based on Avg Qty (Man)
                self._update_avg_qty_adj(sorted_adj_products)
        if self.procure_lt:
            buy_prod_dict, produce_products = self._get_leadtime_data(sorted_products)
            buy_prod_dict = self._update_buy_prod_procure_lt(buy_prod_dict, from_date)
            self._update_produce_prod_procure_lt(buy_prod_dict, produce_products)
        return {"type": "ir.actions.act_window_close"}

    @api.multi
    def clear_manual_fields(self):
        self.ensure_one()
        self.env.cr.execute(
            """
            UPDATE product_product
            SET avg_qty_man = 0
            WHERE avg_qty_man > 0
            """
        )
        self.env.cr.execute(
            """
            UPDATE product_product
            SET proc_lt_man = 0
            WHERE proc_lt_man > 0
            """
        )
        return {"type": "ir.actions.act_window_close"}
