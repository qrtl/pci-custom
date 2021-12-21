# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = "product.product"

    avg_qty_needed = fields.Float(
        "Average Qty Needed (per Month)",
        digits=dp.get_precision("Product Unit of Measure"),
        readonly=True,
        help="Calculated based on the outgoing moves in the recent periods, which is "
        "based on 'No. of Months for Procurement Calc.' in the company.",
    )
    avg_qty_adj = fields.Float(
        "Adjusted Qty", digits=dp.get_precision("Product Unit of Measure"),
    )
    avg_qty_adj_comp = fields.Float(
        "Average Qty Needed (Adjusted)",
        digits=dp.get_precision("Product Unit of Measure"),
        readonly=True,
        help="Calculated based on 'Avg Qty Needed' and 'Adjusted Qty'. Takes the "
        "number from 'Adjusted Qty' if available, otherwise from 'Avg Qty Needed'.",
    )
    proc_lt_calc = fields.Float(
        "Procurement LT (Calculated)",
        readonly=True,
        help="Number of months required to procure the product. Calculated based on "
        "the transaction history in the recent periods which is based on 'No. of "
        "Months for Procurement Calc.' in the company.",
    )
    proc_lt_manu = fields.Float("Procurement LT (Manual)")
    qty_suggested = fields.Float(
        compute="_compute_qty",
        string="Suggested Stock Qty",
        digits=dp.get_precision("Product Unit of Measure"),
    )
    qty_variance = fields.Float(
        compute="_compute_qty",
        string="Variance",
        digits=dp.get_precision("Product Unit of Measure"),
    )

    @api.multi
    def _compute_qty(self):
        for prod in self:
            if prod.avg_qty_adj_comp:
                avg_qty = prod.avg_qty_adj_comp
            elif prod.avg_qty_adj:
                avg_qty = prod.avg_qty_adj
            else:
                avg_qty = prod.avg_qty_needed
            if prod.proc_lt_manu:
                proc_lt = prod.proc_lt_manu
            else:
                proc_lt = prod.proc_lt_calc
            prod.qty_suggested = avg_qty * proc_lt
            prod.qty_variance = prod.qty_available + prod.incoming_qty - \
                                prod.qty_suggested
