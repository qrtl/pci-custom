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

from openerp.osv import osv, fields
from openerp.tools.translate import _


class sale_shop(osv.osv):
    _inherit = 'sale.shop'
    
    _columns= {
        'shipment_day': fields.selection([('0', 'Monday'),
                                          ('1', 'Tuesday'),
                                          ('2', 'Wednesday'),
                                          ('3', 'Thursday'),
                                          ('4', 'Friday'), 
                                          ('5', 'Saturday'),
                                          ('6', 'Sunday')], string='Shipment Day'),
    }
