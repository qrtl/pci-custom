# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class stock_inventory(osv.osv):
    _inherit = "stock.inventory"

    def action_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for inv in self.browse(cr, uid, ids, context=context):
            serial_dict = {}
            for move in inv.inventory_line_id:
                if move.prod_lot_id and move.prod_lot_id.id not in serial_dict:
                    serial_dict[move.prod_lot_id.id] = 1
                elif move.prod_lot_id and move.prod_lot_id.id in serial_dict:
                    serial_dict[move.prod_lot_id.id] += 1
            for serial in serial_dict:
                if serial_dict[serial] > 1:
                    serial_data = self.pool.get('stock.production.lot').browse(cr, uid, [serial], context)[0]
                    if serial_data.product_id.product_tmpl_id.categ_id.enforce_qty_1:
                        raise osv.except_osv(_('Error!'),
                                         _('Sorry, You can not have serial number same for multiple inventory lines - [%s]')
                                                        % serial_data.name)
        return super(stock_inventory, self).action_confirm(cr, uid, ids, context=context)

class stock_picking(osv.osv):
    _inherit = "stock.picking"

    def action_done(self, cr, uid, ids, context=None):
        pickings = self.browse(cr, uid, ids, context=context)
        for picking in pickings:
            serial_dict = {}
            for move in picking.move_lines:
                if move.prodlot_id and move.prodlot_id.id not in serial_dict:
                    serial_dict[move.prodlot_id.id] = 1
                elif move.prodlot_id and move.prodlot_id.id in serial_dict:
                    serial_dict[move.prodlot_id.id] += 1
            for serial in serial_dict:
                if serial_dict[serial] > 1:
                    serial_data = self.pool.get('stock.production.lot').browse(cr, uid, [serial], context)[0]
                    if serial_data.product_id.product_tmpl_id.categ_id.enforce_qty_1:
                        raise osv.except_osv(_('Error!'),
                                         _('Sorry, You can not have serial number same for multiple move lines - [%s]')
                                                        % serial_data.name)
        return super(stock_picking, self).action_done(cr, uid, ids, context=context)

class stock_move(osv.osv):
    _inherit = 'stock.move'

    def action_done(self, cr, uid, ids, context=None):
        res = super(stock_move, self).action_done(cr, uid, ids, context)
        if context is None:
            context = {}
        for move in self.browse(cr, uid, ids, context):
            if move.product_id.product_tmpl_id.categ_id.enforce_qty_1 and move.product_qty > 1.0 and move.prodlot_id:
                raise osv.except_osv(_('Error!'), _('Quantity of stock move should be 1 for product %s (enforce quantity 1).') 
                                                % move.product_id.name)
            if move.sale_line_id and not move.sale_line_id.serial_id and move.prodlot_id:
                self.pool.get('sale.order.line').write(cr, uid, [move.sale_line_id.id], {'serial_id': move.prodlot_id.id}, context)
                invoice_line_ids = [line.id for line in move.sale_line_id.invoice_lines] 
                self.pool.get('account.invoice.line').write(cr, uid, invoice_line_ids, {'serial_id':move.prodlot_id.id}, context)
        return res

class stock_model(osv.osv):
    _name = 'stock.model'

    _columns = {
        'name': fields.char('Name', required=True),
        'sequence': fields.integer('Sequence'),
    }

    _defaults = {
        'sequence': 5,
    }

class stock_body(osv.osv):
    _name = 'stock.body'

    _columns = {
        'name': fields.char('Name', required=True),
    }

class stock_neck(osv.osv):
    _name = 'stock.neck'

    _columns = {
        'name': fields.char('Name', required=True),
    }

class stock_pickguard(osv.osv):
    _name = 'stock.pickguard'

    _columns = {
        'name': fields.char('Name', required=True),
    }

class stock_shop(osv.osv):
    _name = 'stock.shop'

    _columns = {
        'name': fields.char('Name', required=True),
    }

class stock_production_lot(osv.osv):
    _inherit = "stock.production.lot"
    _order = 'sequence'

    def onchange_weightlb(self, cr, uid, ids, product_id, weight_lb, lb_uom_id, context=None):
        if lb_uom_id:
            uom = self.pool.get('product.uom').browse(cr, uid, lb_uom_id, context=context)
            kg = weight_lb/uom.factor
            return {'value': {'weight_kg': kg}}
        return {}

    def onchange_product_id(self, cr, uid, ids, body_id, neck_id, pickguard_id, product_id, context=None):
        res = {}
        if not product_id:
            return {}
        product_default_code = self.pool.get('product.product').browse(cr, uid, product_id, context=context).default_code or ''
        res.update({'ref': product_default_code})
        res_prefix = self.onchange_prefix(cr, uid, ids, body_id, neck_id, pickguard_id, product_id)
        res.update(res_prefix['value'])
        return {'value': res}

    def onchange_prefix(self, cr, uid, ids, body_id, neck_id, pickguard_id, product_id, context=None):
        body_obj = self.pool.get('stock.body')
        neck_obj = self.pool.get('stock.neck')
        pickguard_obj = self.pool.get('stock.pickguard')
        product_obj = self.pool.get('product.product')
        name = ''
        if product_id:
            product_name = product_obj.browse(cr, uid, product_id, context=context).name
            if product_name:
                name = name + product_name + '/'
        if body_id:
            body_name = body_obj.browse(cr, uid, body_id, context=context).name
            if body_name:
                name = name + body_name + '/'
        if neck_id:
            neck_name = neck_obj.browse(cr, uid, neck_id, context=context).name
            if neck_name:
                name = name + neck_name + '/'
        if pickguard_id:
            pickguard_name = pickguard_obj.browse(cr, uid, pickguard_id, context=context).name
            if pickguard_name:
                name = name + pickguard_name
#         name = product_name + '/' + body_name + '/' + neck_name + '/' + pickguard_name
        return {'value': {'prefix': name}}

    def _get_lb_unit(self, cr, uid, context=None):
        if context is None:
            context = {}
        md = self.pool.get('ir.model.data')
        res = False
        try:
            res = md.get_object_reference(cr, uid, 'stock_serial_number', 'product_uom_lbs')[1]
        except ValueError:
            res = False
        return res

    def _get_kg_unit(self, cr, uid, context=None):
        if context is None:
            context = {}
        md = self.pool.get('ir.model.data')
        res = False
        try:
            res = md.get_object_reference(cr, uid, 'product', 'product_uom_kgm')[1]
        except ValueError:
            res = False
        return res

    def _get_sequence(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        sequence = 0
        for lot in self.browse(cr, uid, ids, context=context):
            if lot.model_id:
                sequence = lot.model_id.sequence
            res[lot.id] = sequence
        return res

    def _get_reserved_qty(self, cr, uid, ids, field_name, args, context=None):
        uom_obj = self.pool.get('product.uom')
        res = {}
        reserved_qty = 0.0
        for lot in self.browse(cr, uid, ids, context=context):
            for move in lot.move_ids:
                if move.state in ('confirmed', 'assigned') and \
                    move.location_dest_id.usage == 'customer':
                    reserved_qty += move.product_qty
            res[lot.id] = reserved_qty 
        return res

    _columns = {
        'product_name': fields.related('product_id', 'name', type='char', relation='product.product', string='Product', readonly=True),
        'track_outgoing': fields.related('product_id', 'track_outgoing', type='boolean', relation='product.product', string='Track Outgoing Lots'),
        'list_price': fields.float('Sale Price', digits_compute=dp.get_precision('Product Price')),
        'standard_price': fields.float('Cost Price', digits_compute=dp.get_precision('Product Price'), groups="base.group_user"),
        'model_id': fields.many2one('stock.model', 'Model'),
        'sequence': fields.function(_get_sequence, type='integer', string="Sequence", store=True),
        'body_id': fields.many2one('stock.body', 'Body'),
        'neck_id': fields.many2one('stock.neck', 'Neck'),
        'pickguard_id': fields.many2one('stock.pickguard', 'Pickguard'),
        'shop_ids': fields.many2many('stock.shop', 'rel_stock_shop', 'stock_production_lot_id', 'rel_lot_id', 'Shop'),
        'check': fields.selection([('deliver', u'★'), ('rework', u'▲')], 'Check'),
        'hri': fields.boolean('HRI'),
        'note1': fields.char('Note 1'),
        'note2': fields.char('Note 2'),
        'note3': fields.char('Note 3'),
        'weight_lb': fields.float('Weight (lb)'),
        'weight_kg': fields.float('Weight (kg)'),
        'lb_uom_id' : fields.many2one('product.uom', 'Unit of Measure (lb)'),
        'kg_uom_id' : fields.many2one('product.uom', 'Unit of Measure (kg)'),
        'reserved_qty': fields.function(_get_reserved_qty, type='float', 
                                        string='Reserved Quantity', 
                                        help="Reserved Quantity by sale order.",
                                        digits_compute=dp.get_precision('Product Unit of Measure')),
        'purchased_qty': fields.float('Purchased Quantity',
                                      help="Purchased Quantity by PO.",
                                      digits_compute=dp.get_precision('Product Unit of Measure')),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        default = {} if default is None else default.copy()
        default.update({
        })
        return super(stock_production_lot, self).copy(cr, uid, id, default=default, context=context)

    def _check_serial_enforce(self, cr, uid, ids, context=None):
        #i. Serial number + product should be unique in serial number master (stock.product.lot)
        for prod in self.browse(cr, uid, ids, context=context):
            if prod.product_id.product_tmpl_id.categ_id.enforce_qty_1:
                lot_ids = self.search(cr, uid, [('id', '!=', prod.id),
                                                ('product_id', '=', prod.product_id.id),
                                                ('name', '=', prod.name)], context)
                if lot_ids:
                    return False
        return True 

    def _check_serial_qty(self, cr, uid, ids, context=None):
        # Qty on hand should not exceed 1 for serial number + product
        for prod in self.browse(cr, uid, ids, context=context):
            if prod.product_id.product_tmpl_id.categ_id.enforce_qty_1:
                if prod.stock_available > 1:
                    return False
        return True

    _constraints = [
        (_check_serial_enforce, 'Error! Serial number must be unique for \
            product with "ENFORCE QTY 1" setting.', ['name', 'product_id']),
        (_check_serial_qty, 'Error! Quantity on hand should not exceed 1 for \
            product with "ENFORCE QTY 1" setting.', ['stock_available'])
    ]

    _defaults = {
        'lb_uom_id' : _get_lb_unit,
        'kg_uom_id' : _get_kg_unit,
        'purchased_qty': 0.0,
    }
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
