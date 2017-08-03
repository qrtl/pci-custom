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
    fixed_price = fields.Boolean(
        'Fixed Price',
        help='No price recomputation if selected.',
    )
    price_unit = fields.Float(
        'Unit Price',
        required=True,
        digits=dp.get_precision('Product Price'),
        default=0.0,
        compute='_recompute_price_unit',
        inverse='_inverse_price_unit',
        store=True,
    )
    price_unit_manual = fields.Float(
        'Unit Price (Manual)',
        digits=dp.get_precision('Product Price'),
        default=0.0,
        compute='_update_price_unit_manual',
        store=True,
    )


    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if self.fixed_price:
            return
        else:
            return super(SaleOrderLine, self).product_uom_change()

    @api.multi
    @api.depends('fixed_price')
    def _update_price_unit_manual(self):
        for l in self:
            if l.fixed_price:
                l.price_unit_manual = l.price_unit
            else:
                l.price_unit_manual = 0.0

    @api.multi
    @api.depends('price_categ_qty')
    def _recompute_price_unit(self):
        for l in self:
            if l.fixed_price:
                l.price_unit = l.price_unit_manual
            else:
                # following code is taken from:
                # https://github.com/odoo/odoo/blob/5ed09bc17c5ccff66e08ccd1d6\
                # ad89b0cc070b21/addons/sale/models/sale.py#L911-L926
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
        line_dict = {}
        for line in self:
            if not line.id in line_dict:
                categ_lines = line.order_id.order_line.filtered(
                    lambda x: x.price_categ_id and
                              x.price_categ_id == line.price_categ_id)
                categ_qty = sum(r.product_uom_qty for r in categ_lines)
                if categ_lines:
                    for l in categ_lines:
                        if not l in line_dict:
                            line_dict[l.id] = categ_qty
                    line.price_categ_qty = categ_qty
                else:
                    line.price_categ_qty = line.product_uom_qty
            else:
                line.price_categ_qty = line_dict[line.id]

    def _inverse_price_unit(self):
        for l in self:
            if l.fixed_price:
                l.price_unit_manual = l.price_unit

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
