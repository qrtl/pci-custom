# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    @api.onchange('lot_id')
    def lot_id_change(self):
        if self.lot_id:
            self.price_unit = self.lot_id.list_price
        elif self.product_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id.id,
                quantity=self.product_uom_qty or 1.0,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id
            )
            if self.order_id.pricelist_id and self.order_id.partner_id:
                self.price_unit = self.env['account.tax'].\
                    _fix_tax_included_price(self._get_display_price(product),
                                            product.taxes_id, self.tax_id)

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if self.lot_id:
            self.price_unit = self.lot_id.list_price
        else:
            super(SaleOrderLine, self).product_uom_change()

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res['lot_id'] = self.lot_id.id
        return res
