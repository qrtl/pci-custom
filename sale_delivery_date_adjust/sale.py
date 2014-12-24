# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Rooms For (Hong Kong) Limited T/A OSCG
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

from openerp.osv import fields, osv
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta


class sale_order(osv.osv):
    _inherit = 'sale.order'

    def _get_date_planned(self, cr, uid, order, line, start_date, context=None):
        categ_lt = 0
        date_order = datetime.strptime(order.date_order, '%Y-%m-%d')
        if not order.name.encode('ascii','ignore').startswith('SO'):  # manually created SO should start with 'SO'
            categ_obj = self.pool.get('res.partner.category')
            categ_ids = categ_obj.search(cr, uid, [('partner_ids','in',order.partner_id.id),('scheduled_time','=',True)])
            # in case partner is the contact person without relevant category assignment
            if not categ_ids and order.partner_id.parent_id:
                categ_ids = categ_obj.search(cr, uid, [('partner_ids','in',order.partner_id.parent_id.id),('scheduled_time','=',True)])
            for categ in categ_obj.browse(cr, uid, categ_ids):
                if not categ.cutoff:
                    categ_lt = categ.days_added
                else:
                    cutoff_day = int(categ.cutoff_day)  # convert from char to integer
                    if date_order.weekday() <= cutoff_day:  # weekday(): 0=Monday, 6=Sunday
                        categ_lt = cutoff_day - date_order.weekday() + categ.days_added
                    else:
                        categ_lt = cutoff_day - date_order.weekday() + 7 + categ.days_added
        return datetime.strftime(date_order + relativedelta(days=categ_lt), '%Y-%m-%d')

sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
