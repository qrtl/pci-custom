# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"
    _order = 'sequence'

    product_name = fields.Char(
        related='product_id.name',
        string='Product',
        readonly=True
    )
    prefix = fields.Char()
    tracking = fields.Selection(related='product_id.tracking')
    list_price = fields.Float(
        'Sale Price',
        digits_compute=dp.get_precision('Product Price')
    )
    standard_price = fields.Float(
        'Cost Price',
        digits_compute=dp.get_precision('Product Price'),
        groups="base.group_user"
    )
    model_id = fields.Many2one(
        comodel_name='stock.model',
        string='Model',
    )
    sequence = fields.Integer(
        related='model_id.sequence',
        # store=True,
    )
    body_id = fields.Many2one(
        comodel_name='stock.body',
        string='Body'
    )
    neck_id = fields.Many2one(
        comodel_name='stock.neck',
        string='Neck'
    )
    pickguard_id = fields.Many2one(
        comodel_name='stock.pickguard',
        string='Pickguard'
    )
    shop_ids = fields.Many2many(
        comodel_name='stock.shop',
        string='Shop',
    )
    check = fields.Selection(
        [('deliver', u'★'),
         ('rework', u'▲')],
    )
    hri = fields.Boolean('HRI')
    note1 = fields.Char('Note 1')
    note2 = fields.Char('Note 2')
    note3 = fields.Char('Note 3')
    weight_lb = fields.Float('Weight (lb)')
    weight_kg = fields.Float('Weight (kg)')
    lb_uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='Unit of Measure (lb)'
    )
    kg_uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='Unit of Measure (kg)'
    )
    reserved_qty = fields.Float(
        compute='_get_reserved_qty',
        string='Reserved Quantity',
        help="Quantity reserved by sales order.",
        digits_compute=dp.get_precision('Product Unit of Measure')
    )
    purchased_qty = fields.Float(
        string='Purchased Quantity',
        digits_compute=dp.get_precision('Product Unit of Measure')
    )


#     def onchange_weightlb(self, cr, uid, ids, product_id, weight_lb, lb_uom_id, context=None):
#         if lb_uom_id:
#             uom = self.pool.get('product.uom').browse(cr, uid, lb_uom_id, context=context)
#             kg = weight_lb/uom.factor
#             return {'value': {'weight_kg': kg}}
#         return {}
#
#     def onchange_product_id(self, cr, uid, ids, body_id, neck_id, pickguard_id, product_id, context=None):
#         res = {}
#         if not product_id:
#             return {}
#         product_default_code = self.pool.get('product.product').browse(cr, uid, product_id, context=context).default_code or ''
#         res.update({'ref': product_default_code})
#         res_prefix = self.onchange_prefix(cr, uid, ids, body_id, neck_id, pickguard_id, product_id)
#         res.update(res_prefix['value'])
#         return {'value': res}
#
#     def onchange_prefix(self, cr, uid, ids, body_id, neck_id, pickguard_id, product_id, context=None):
#         body_obj = self.pool.get('stock.body')
#         neck_obj = self.pool.get('stock.neck')
#         pickguard_obj = self.pool.get('stock.pickguard')
#         product_obj = self.pool.get('product.product')
#         name = ''
#         if product_id:
#             product_name = product_obj.browse(cr, uid, product_id, context=context).name
#             if product_name:
#                 name = name + product_name + '/'
#         if body_id:
#             body_name = body_obj.browse(cr, uid, body_id, context=context).name
#             if body_name:
#                 name = name + body_name + '/'
#         if neck_id:
#             neck_name = neck_obj.browse(cr, uid, neck_id, context=context).name
#             if neck_name:
#                 name = name + neck_name + '/'
#         if pickguard_id:
#             pickguard_name = pickguard_obj.browse(cr, uid, pickguard_id, context=context).name
#             if pickguard_name:
#                 name = name + pickguard_name
# #         name = product_name + '/' + body_name + '/' + neck_name + '/' + pickguard_name
#         return {'value': {'prefix': name}}
#
#     def _get_lb_unit(self, cr, uid, context=None):
#         if context is None:
#             context = {}
#         md = self.pool.get('ir.model.data')
#         res = False
#         try:
#             res = md.get_object_reference(cr, uid, 'stock_serial_number', 'product_uom_lbs')[1]
#         except ValueError:
#             res = False
#         return res
#
#     def _get_kg_unit(self, cr, uid, context=None):
#         if context is None:
#             context = {}
#         md = self.pool.get('ir.model.data')
#         res = False
#         try:
#             res = md.get_object_reference(cr, uid, 'product', 'product_uom_kgm')[1]
#         except ValueError:
#             res = False
#         return res

    @api.multi
    def _get_reserved_qty(self):
        for lot in self:
            quants = self.env['stock.quant'].search(
                [('lot_id', '=', lot.id),
                 ('reservation_id', '!=', False)])
            lot.reserved_qty = sum(q.qty for q in quants)

#
#
#     def copy(self, cr, uid, id, default=None, context=None):
#         default = {} if default is None else default.copy()
#         default.update({
#         })
#         return super(stock_production_lot, self).copy(cr, uid, id, default=default, context=context)
#
#     def _check_serial_enforce(self, cr, uid, ids, context=None):
#         #i. Serial number + product should be unique in serial number master (stock.product.lot)
#         for prod in self.browse(cr, uid, ids, context=context):
#             if prod.product_id.product_tmpl_id.categ_id.enforce_qty_1:
#                 lot_ids = self.search(cr, uid, [('id', '!=', prod.id),
#                                                 ('product_id', '=', prod.product_id.id),
#                                                 ('name', '=', prod.name)], context)
#                 if lot_ids:
#                     return False
#         return True
#
#     def _check_serial_qty(self, cr, uid, ids, context=None):
#         # Qty on hand should not exceed 1 for serial number + product
#         for prod in self.browse(cr, uid, ids, context=context):
#             if prod.product_id.product_tmpl_id.categ_id.enforce_qty_1:
#                 if prod.stock_available > 1:
#                     return False
#         return True
#
#     _constraints = [
#         (_check_serial_enforce, 'Error! Serial number must be unique for \
#             product with "ENFORCE QTY 1" setting.', ['name', 'product_id']),
#         (_check_serial_qty, 'Error! Quantity on hand should not exceed 1 for \
#             product with "ENFORCE QTY 1" setting.', ['stock_available'])
#     ]
#
#     _defaults = {
#         'lb_uom_id' : _get_lb_unit,
#         'kg_uom_id' : _get_kg_unit,
#         'purchased_qty': 0.0,
#     }
