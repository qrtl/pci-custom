# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    price_categ_id = fields.Many2one(
        comodel_name='product.category',
        compute='_get_price_categ_id',
        store=True,
        string='Category for Pricing',
    )
    price_categ_qty = fields.Float(
        compute='_compute_price_categ_qty',
        store=True,
        string='Category Qty for Pricing',
    )
    price_unit = fields.Float(
        'Unit Price',
        required=True,
        digits=dp.get_precision('Product Price'),
        default=0.0,
        compute='_recompute_price_unit',
        store=True,
    )

    @api.multi
    @api.depends('product_id')
    def _get_price_categ_id(self):
        for l in self.filtered('product_id'):
            # FIXME may need to avoid assigning price_categ_id in case
            # the product varient/template appears in pricelist lines
            categs = l.order_id.pricelist_id.item_ids.filtered(
                lambda x: x.applied_on == '2_product_category' and
                x.min_quantity > 1).mapped('categ_id')
            if categs:
                categ = l.product_id.categ_id
                while categ:
                    if categ in categs:
                        l.price_categ_id = categ
                        categ = False
                    else:
                        categ = categ.parent_id

    @api.multi
    @api.depends('price_categ_qty')
    def _recompute_price_unit(self):
        for l in self:
            # following code is taken from:
            # https://github.com/odoo/odoo/blob/5ed09bc17c5ccff66e08ccd1d6ad89\
            # b0cc070b21/addons/sale/models/sale.py#L911-L926
            # the only difference is quantity assignment in context - use
            # price_categ_qty instead of product_uom_qty
            product = l.product_id.with_context(
                lang=l.order_id.partner_id.lang,
                partner=l.order_id.partner_id.id,
                quantity=l.price_categ_qty,
                date_order=l.order_id.date_order,
                pricelist=l.order_id.pricelist_id.id,
                uom=l.product_uom.id,
                fiscal_position=l.env.context.get(
                    'fiscal_position')
            )
            l.price_unit = self.env['account.tax']._fix_tax_included_price(
                l._get_display_price(product), product.taxes_id, l.tax_id)

    @api.multi
    @api.depends('order_id.order_line.price_categ_id',
                 'order_id.order_line.product_uom_qty')
    def _compute_price_categ_qty(self):
        for line in self:
            # FIXME improve algorithm to avoid redundancy
            categ_lines = line.order_id.order_line.filtered(
                lambda x: x.price_categ_id and
                          x.price_categ_id == line.price_categ_id)
            categ_qty = sum(r.product_uom_qty for r in categ_lines)
            if categ_lines:
                for l in categ_lines.filtered(
                        lambda x: x.price_categ_qty != categ_qty):
                    l.price_categ_qty = categ_qty
            else:
                line.price_categ_qty = line.product_uom_qty
