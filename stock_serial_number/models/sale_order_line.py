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
        else:
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

    #
    # def _prepare_order_line_invoice_line(self, cr, uid, line, account_id = False, context=None):
    #     res = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line=line,
    #                                                                         account_id = account_id,
    #                                                                         context = context)
    #     res.update({'serial_id': line.serial_id.id})
    #     return res
