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

    @api.multi
    def _preppare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res['lot_id'] = self.lot_id.id

                    #
    # def _prepare_order_line_invoice_line(self, cr, uid, line, account_id = False, context=None):
    #     res = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line=line,
    #                                                                         account_id = account_id,
    #                                                                         context = context)
    #     res.update({'serial_id': line.serial_id.id})
    #     return res


    # @api.multi
    # def _prepare_invoice_line(self, qty):
    #     """
    #     Prepare the dict of values to create the new invoice line for a sales order line.
    #
    #     :param qty: float quantity to invoice
    #     """
    #     self.ensure_one()
    #     res = {}
    #     account = self.product_id.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id
    #     if not account:
    #         raise UserError(_(
    #             'Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
    #                         (self.product_id.name, self.product_id.id,
    #                          self.product_id.categ_id.name))
    #
    #     fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
    #     if fpos:
    #         account = fpos.map_account(account)
    #
    #     res = {
    #         'name': self.name,
    #         'sequence': self.sequence,
    #         'origin': self.order_id.name,
    #         'account_id': account.id,
    #         'price_unit': self.price_unit,
    #         'quantity': qty,
    #         'discount': self.discount,
    #         'uom_id': self.product_uom.id,
    #         'product_id': self.product_id.id or False,
    #         'layout_category_id': self.layout_category_id and self.layout_category_id.id or False,
    #         'product_id': self.product_id.id or False,
    #         'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
    #         'account_analytic_id': self.order_id.project_id.id,
    #         'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
    #     }
    #     return res
