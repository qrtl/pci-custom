# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"
    _order = 'sequence'

    def _default_lb_unit(self):
        md = self.env['ir.model.data']
        try:
            res = md.get_object_reference(
                'product', 'product_uom_lb')[1]
        except ValueError:
            res = False
        return res

    def _default_kg_unit(self):
        md = self.env['ir.model.data']
        try:
            res = md.get_object_reference(
                'product', 'product_uom_kgm')[1]
        except ValueError:
            res = False
        return res

    name = fields.Char(copy=False)
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
        string='Unit of Measure (lb)',
        default=_default_lb_unit,
    )
    kg_uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='Unit of Measure (kg)',
        default=_default_kg_unit,
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
    stock_available = fields.Float(
        compute='_compute_balance',
        store=True,
        string='Available',
        readonly=True,
    )

    @api.one
    @api.depends('product_id', 'ref', 'quant_ids.qty', 'quant_ids.location_id')
    def _compute_balance(self):
        int_locs = self.env['stock.location'].search(
            [('usage', '=', 'internal')])
        loc_ids = [loc.id for loc in int_locs]
        quants = self.env['stock.quant'].search(
            [('lot_id', '=', self.id),
             ('product_id', '=', self.product_id.id),
             ('location_id', 'in', loc_ids)]
        )
        for q in quants:
            self.stock_available += q.qty

    @api.onchange('weight_lb', 'lb_uom_id')
    def _get_weight_kg(self):
        if self.lb_uom_id:
            self.weight_kg = self.weight_lb / self.lb_uom_id.factor

    @api.onchange('product_id')
    def onchange_product(self):
        if not self.product_id:
            self.ref = False
        else:
            self.ref = self.product_id.default_code

    @api.onchange('product_id', 'body_id', 'neck_id', 'pickguard_id')
    def _get_prefix(self):
        name = ''
        if self.product_id:
            name += self.product_id.name + '/'
        if self.body_id:
            name += self.body_id.name + '/'
        if self.neck_id:
            name += self.neck_id.name + '/'
        if self.pickguard_id:
            name += self.pickguard_id.name
        self.prefix = name

    @api.multi
    def _get_reserved_qty(self):
        for lot in self:
            quants = self.env['stock.quant'].search(
                [('lot_id', '=', lot.id),
                 ('reservation_id', '!=', False)])
            lot.reserved_qty = sum(q.qty for q in quants)

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            name = rec.name
            prefix = rec.prefix
            if prefix:
                name = prefix + '/' + name
            if rec.ref:
                name = '%s [%s]' % (name, rec.ref)
            res.append((rec.id, name))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name),
                      ('prefix', operator, name)]
        serials = self.search(domain + args, limit=limit)
        return serials.name_get()
