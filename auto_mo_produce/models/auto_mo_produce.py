# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import datetime
from openerp.osv import fields, osv
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

class mo_auto_produce_rules(osv.osv):
    _name = 'mo.auto.produce.rules'
    
    _columns = {
        'product_category_ids': fields.many2many('product.category',
                                                 'mrp_production_product_category',
                                                 'production_id',
                                                 'category_id',
                                                 'Product Category',
                                                 required=True,),
        'source_location_id': fields.many2one('stock.location',
                                              'Raw Materials Location',
                                              required=True,),
        'destination_location_id': fields.many2one('stock.location',
                                                   'Finished Products Location',
                                                   required=True,),
        'active': fields.boolean('Active'),
    }

    _defaults = {
        'active': True
         }

class mrp_production(osv.osv):
    _inherit = 'mrp.production'

    def process_mo_produce(self, cr, uid, ids=None, context=None):
        rules_obj = self.pool.get('mo.auto.produce.rules')
        rules_ids = rules_obj.search(cr, uid, [('active', '=', True)], context=context)
        today = datetime.datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        mo_ids = self.search(cr, uid, [('date_planned', '<=', today),
                                       ('state', '=', 'ready')], context=context)
        produced_mo = []
        for mo in self.browse(cr, uid, mo_ids, context=context):
            mo_product_category = mo.product_id.categ_id
            for rule in rules_obj.browse(cr, uid, rules_ids, context=context):
                if mo.location_src_id.id == rule.source_location_id.id and\
                    mo.location_dest_id.id == rule.destination_location_id.id and\
                    mo_product_category in rule.product_category_ids:
                        if mo.id not in produced_mo:
                            self.action_produce(cr, uid, mo.id,
                                                mo.product_qty, 'consume_produce',
                                                context=context)
                            produced_mo.append(mo.id)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: