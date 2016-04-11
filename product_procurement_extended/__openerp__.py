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

{
    'name': 'Product Procurement Extended',
    'version': '7.0.1.1.0',
    'category': 'Product',
    'summary': '',
    'description': """
Main Features
-------------
1. Adds procurement related fields to product.
2. Adds a menu item to open a wizard to run updates on procurement related fields in product.
3. Adds a menu item to open a product tree view tailored to show procurement related info.
 
     """,
    'author': 'Rooms For (Hong Kong) T/A OSCG',
    'depends': ['purchase', 'mrp'],
    'init_xml': [],
    'data': [
        'wizard/product_procurement.xml',
        'res_config_view.xml',
        'company_view.xml',
        'security/product_security.xml',
        'product_view.xml',
    ],
   
    'demo_xml': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
