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

{
    'name': 'Stock Physical Inventory Adjust',
    'version': '0.5',
    'category': 'Stock',
    'description': """

Overview:
===============================

* Adds "Date Done" field in Physical Inventories screen.
* Note that "Date Done" field (`date_done`) is currently added to stock/stock.py by directly modifying the original code.

    """,
    'author': 'Rooms For (Hong Kong) Limited T/A OSCG',
    'website': 'http://www.openerp-asia.net/',
    'depends': ['stock'],
    'data': [
        'stock_view.xml',
        ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
