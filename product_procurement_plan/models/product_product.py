# -*- coding: utf-8 -*-
# Copyright 2017-2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = "product.product"

    avg_qty_calc = fields.Float(
        "Average Qty (Calculated)",
        digits=dp.get_precision("Product Unit of Measure"),
        readonly=True,
        help="Calculated based on the recent outgoing shipments of the parent product "
        "for the given number of months.",
    )
    avg_qty_man = fields.Float(
        "Average Qty (Manual)",
        digits=dp.get_precision("Product Unit of Measure"),
        help="Manual modification to the computed result of Average Qty "
        "(Calculated). The value affects the result of Average Qty (Adjusted) in "
        "Product Proc. Info Update. Note that it affects the computation for the lower "
        "level components as well.",
    )
    avg_qty_adj = fields.Float(
        "Average Qty (Adjusted)",
        digits=dp.get_precision("Product Unit of Measure"),
        readonly=True,
        help="Adjusted quantity to 'Average Qty (Calculated)' with consideration of "
        "'Average Qty (Manual)'.",
    )
    proc_lt_calc = fields.Float(
        "Lead Time (Calculated)",
        readonly=True,
        help="Number of months required to procure the product. Calculated based on "
        "the transaction history for the given number of months.",
    )
    proc_lt_man = fields.Float(
        "Lead Time (Manual)",
        help="Manual modification to the computed result of Lead Time (Calculated). "
        "The input value instantly affects the value of 'Lead Time (Adjusted)'.",
    )
    proc_lt_adj = fields.Float(
        "Lead Time (Adjusted)",
        compute="_compute_proc_lt_adj",
    )
    qty_suggested = fields.Float(
        compute="_compute_qty_variance",
        string="Suggested Stock Qty",
        digits=dp.get_precision("Product Unit of Measure"),
        help="Suggested stock quantity based on the calculation of Average Qty "
        "(Adjusted) * Lead Time (Adjusted)'",
    )
    qty_variance = fields.Float(
        compute="_compute_qty_variance",
        string="Variance",
        digits=dp.get_precision("Product Unit of Measure"),
    )

    @api.multi
    def _compute_proc_lt_adj(self):
        for product in self:
            if product.proc_lt_man:
                product.proc_lt_adj = product.proc_lt_man
            else:
                product.proc_lt_adj = product.proc_lt_calc

    @api.multi
    def _compute_qty_variance(self):
        for product in self:
            product.qty_suggested = product.avg_qty_adj * product.proc_lt_adj
            product.qty_variance = product.qty_available + product.incoming_qty - product.qty_suggested
