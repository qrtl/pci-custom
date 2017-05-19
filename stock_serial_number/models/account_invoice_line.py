# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models, fields
# from odoo.addons import decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    lot_id = fields.Many2one(
        comodel_name='stock.production.lot',
        string='Serial Number'
    )

    """to be deleted later """
    # standard_price = fields.Float(
    #     related='lot_id.standard_price',
    #     string='Cost Price',
    #     digits_compute=dp.get_precision('Product Price'),
    #     groups="base.group_user"
    # )
    # serial_standard_price = fields.Float(
    #     'Cost Price',
    #     digits_compute=dp.get_precision('Product Price'),
    #     groups="base.group_user",
    #     readonly=True
    # )
    #
    # def copy(self, cr, uid, id, default=None, context=None):
    #     default = {} if default is None else default.copy()
    #     default.update({
    #         'serial_id':False,
    #         'serial_standard_price': 0.0,
    #     })
    #     return super(account_invoice_line, self).copy(cr, uid, id, default=default, context=context)
