# -*- coding: utf-8 -*-
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

from openerp.osv import fields, osv


class stock_config_settings(osv.osv_memory):
    _inherit = "stock.config.settings"
    
    _columns = {
        'group_stock_procurement_extended': fields.boolean("Allow manual adjustments to needed quantities (Product "
                                                          "Proc. Info)",
           implied_group='product_procurement_extended.group_procurement_extended',
           help="""Columns will be added in Product Proc. Info screen"""),
    }
