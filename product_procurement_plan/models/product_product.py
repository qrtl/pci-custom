# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = "product.product"

    avg_qty_needed = fields.Float(
        'Average Qty Needed (per Month)',
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True
    )
    avg_qty_adj = fields.Float(
        'Adjusted Qty',
        digits=dp.get_precision('Product Unit of Measure'),
    )
    avg_qty_adj_comp = fields.Float(
        'Average Qty Needed (Adjusted)',
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True
    )
    proc_lt_calc = fields.Float(
        'Procurement LT (Calculated)',
        readonly=True
    )
    proc_lt_manu = fields.Float(
        'Procurement LT (Manual)'
    )
    qty_suggested = fields.Float(
        compute="_compute_qty",
        string='Suggested Stock Qty',
        digits=dp.get_precision('Product Unit of Measure'),
    )
    qty_variance = fields.Float(
        compute="_compute_qty",
        string='Variance',
        digits=dp.get_precision('Product Unit of Measure'),
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
            prod.qty_variance = \
                prod.qty_available + prod.incoming_qty - prod.qty_suggested
