# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Rooms For (Hong Kong) Limited T/A OSCG (<http://www.openerp-asia.net>).
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
    'name': 'Sale Stock Serial Number',
    'version': '1.0',
    'author': 'Rooms For (Hong Kong) Ltd T/A OSCG',
    'website': 'http://www.odoo-asia.com',
    'category': 'Sales Management',
    'description': "Sale Stock Serial Number",
    'data': [
            'security/ir.model.access.csv',
            'product_data.xml',
            'stock_view.xml',
            'stock_production_lot_view.xml',
            'sale_view.xml',
            'account_view.xml',
            'product_view.xml',
    ],
    'depends': ['sale', 'stock', 'account_invoice_line_view'],
    'installable': True,
    'auto_install': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
