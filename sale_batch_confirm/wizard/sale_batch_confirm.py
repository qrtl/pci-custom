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

from datetime import datetime, timedelta
import logging

from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

_logger = logging.getLogger(__name__)


class sale_confirm_wizard(osv.osv_memory):
    _name = 'sale.confirm.wizard'
    _columns = {
        'shop_id': fields.many2one('sale.shop', 'Shop',
            help='Quotations with this shop will be filtered for confirmation.'),
        'next_shipment_date': fields.date('Next Shipment Date',
            help='Quotations whose dates are on or before this date will be confirmed.'),
    }


    def _get_next_shipment_date(self, cr, uid, shop_id=False, date=False, context=None):
        shipment_day = int(self.pool.get('sale.shop').browse(cr, uid, shop_id,
            context=context).shipment_day)
        today = datetime.strptime(fields.date.context_today(self, cr, uid,
            context=context), '%Y-%m-%d').date()
        # get the date of next shipment day
        delta = shipment_day - today.weekday()
        if delta < 0:
            delta += 7
        if date:  # when called from scheduled action
            return today + timedelta(days=delta)
        else:  # when called from wizard
            return (today + timedelta(days=delta)).strftime(DEFAULT_SERVER_DATE_FORMAT)


    def onchange_shop_id(self, cr, uid, ids, shop_id=False, context=None):
        res = {}
        if shop_id:
            next_shipment_date = self._get_next_shipment_date(cr, uid, shop_id, False, context)
            res['value'] = {'next_shipment_date': next_shipment_date}
        return res

    
    def _get_default_shop(self, cr, uid, context=None):
        shop_obj = self.pool.get('sale.shop')
        shop_ids = shop_obj.search(cr, uid, [('sale_batch_confirm_default','=',True)])
        if shop_ids:
            for shop in shop_obj.browse(cr, uid, shop_ids, context=context):
                shop_id = shop.id
            return shop_id
    
    _defaults = {
         'shop_id': _get_default_shop
    }


    def _get_sale_ids(self, cr, uid, shop_id, next_shipment_date, context=None):
        return self.pool.get('sale.order').search(cr, uid,
            [('state','in',('draft', 'sent')),
             ('shop_id','=',shop_id),
             ('date_order','<=',next_shipment_date)])

    
    def _batch_confirm_sale(self, cr, uid, sale_ids, conext=None):
        wf_service = netsvc.LocalService('workflow')
        order_confirmed= []
        for order in sale_ids:
            # confirm sales orders
            try:
                wf_service.trg_validate(uid, 'sale.order', order, 'order_confirm', cr)
                order_confirmed.append(order)
            except:
                _logger.info('Order Fail: This order is failed during batch confirm wizard %s' %(order))
        return order_confirmed
        
    
    def batch_confirm_sale_auto(self, cr, uid, context=None):
        shop_obj = self.pool.get('sale.shop')
        shop_ids = shop_obj.search(cr, uid, [('auto_confirm_so','=',True)])
        for shop in shop_obj.browse(cr, uid, shop_ids, context=context):
            next_shipment_date = self._get_next_shipment_date(cr, uid, shop.id, True, context=context)
            sale_ids = self._get_sale_ids(cr, uid, shop.id, next_shipment_date, context=context)
            self._batch_confirm_sale(cr, uid, sale_ids)

    
    def run_wizard(self, cr, uid, ids, context=None):
        for params in self.browse(cr, uid, ids, context=context):
            sale_ids = self._get_sale_ids(cr, uid, params.shop_id.id, params.next_shipment_date, context=context)
            order_confirmed = self._batch_confirm_sale(cr, uid, sale_ids, context)
        # return the list of successfully confirmed sale orders
        return {
            'domain': "[('id','in', ["+','.join(map(str,order_confirmed))+"])]",
            'name': 'Sales Orders',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
