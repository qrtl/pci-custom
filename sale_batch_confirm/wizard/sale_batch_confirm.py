# -*- coding: utf-8 -*-
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Rooms For (Hong Kong) Limited T/A OSCG
#    <https://www.odoo-asia.com>
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

import datetime
import logging

from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc

_logger = logging.getLogger(__name__)


class sale_confirm_wizard(osv.osv_memory):
    _name = 'sale.confirm.wizard'

    def batch_confirm_sale(self, cr, uid, context=None):
        if not context:
            context = {}
        wf_service = netsvc.LocalService('workflow')
        user = self.pool.get('res.users').browse(cr, uid, uid)
        company_id = user.company_id.id
        
        #find the shop of current company
        shop_id = self.pool.get('sale.shop').search(cr, uid, [('company_id', '=', company_id)], context=context)[0]
        shop = self.pool.get('sale.shop').browse(cr, uid, shop_id, context=context)
        shipment_day = shop.shipment_day
        
        today = datetime.date.today()
        #get the sate of net shipment day
        next_shipment_date = today + datetime.timedelta( (int(shipment_day)-today.weekday()) % 7 )
        #find the sale order which has draft stage
        sale_ids = self.pool.get('sale.order').search(cr, uid, [('state', 'in', ('draft', 'sent')), 
                                                                ('name', 'ilike', 'SO'),
                                                                ('date_order', '<=', next_shipment_date)])
        
        sale_orders = self.pool.get('sale.order').browse(cr, uid, sale_ids, context=context)
        order_to_confirm = []
        #filter the sale ids contain only which has name start with SO
        for sale in sale_orders:
            if sale.name.startswith('SO'):
                order_to_confirm.append(sale.id)
        
        order_confirmed= []
        for order in order_to_confirm:
            #confirm the sale orders
            try:
                wf_service.trg_validate(uid, 'sale.order', order, 'order_confirm', cr)
                order_confirmed.append(order)
            except:
                _logger.info('Order Fail: This order is failed during batch confirm wizard %s' %(order))
        return order_confirmed
    
    
    def run_wizard(self, cr, uid, ids, context=None):
        order_confirmed = self.batch_confirm_sale(cr, uid, context)
        #return the list of successfully confirmed sale orders
        return {
            'domain': "[('id','in', ["+','.join(map(str,order_confirmed))+"])]",
            'name': 'Sales Orders',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
