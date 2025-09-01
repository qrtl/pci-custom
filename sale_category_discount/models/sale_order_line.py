# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
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
        store=True,
    )
    # this field has been changed to non-computed field due to the issue
    # described in https://github.com/odoo/odoo/issues/14279
    # e.g. printed quotation from "Send by Email" showed the wrong amount
    # as price_unit_manual was regarded as zero during price recomputation
    price_unit_manual = fields.Float(
        'Unit Price (Manual)',
        digits=dp.get_precision('Product Price'),
        default=0.0,
    )

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if self.fixed_price:
            return
        else:
            return super(SaleOrderLine, self).product_uom_change()

    @api.multi
    def write(self, vals):
        if self.is_delivery:
            if 'price_unit' in vals:
                vals['price_unit_manual'] = vals['price_unit']
        else:
            if vals.get('fixed_price'):
                vals['price_unit_manual'] = vals['price_unit'] \
                    if 'price_unit' in vals else self.price_unit
            elif 'fixed_price' in vals and not vals['fixed_price']:
                vals['price_unit_manual'] = 0.0
            elif self.fixed_price:
                vals['price_unit_manual'] = vals['price_unit'] \
                    if 'price_unit' in vals else self.price_unit
        return super(SaleOrderLine, self).write(vals)

    @api.model
    def create(self, vals):
        if vals.get('fixed_price') or vals.get('is_delivery'):
            vals['price_unit_manual'] = vals.get('price_unit')
        return super(SaleOrderLine, self).create(vals)

    @api.multi
    @api.depends('price_categ_qty')
    def _recompute_price_unit(self):
        for l in self:
            if l.fixed_price or l.is_delivery:
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
                customer_currency = l.order_id.company_id.currency_id
                product_price = customer_currency.compute(
                    product.price, l.order_id.pricelist_id.currency_id)
                l.price_unit = self.env[
                    'account.tax']._fix_tax_included_price(product_price,
                                                           product.taxes_id,
                                                           l.tax_id)

    @api.multi
    @api.depends('order_id.order_line.price_categ_id',
                 'order_id.order_line.product_uom_qty')
    def _compute_price_categ_qty(self):
        line_dict = {}
        for line in self:
            if line.id not in line_dict:
                categ_lines = line.order_id.order_line.filtered(
                    lambda x: x.price_categ_id and
                    x.price_categ_id == line.price_categ_id)
                categ_qty = sum(r.product_uom_qty for r in categ_lines)
                if categ_lines:
                    for l in categ_lines:
                        if l.id not in line_dict:
                            line_dict[l.id] = categ_qty
                    line.price_categ_qty = categ_qty
                else:
                    line.price_categ_qty = line.product_uom_qty
            else:
                line.price_categ_qty = line_dict[line.id]

    @api.multi
    @api.depends('product_id', 'order_id.pricelist_id')
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
