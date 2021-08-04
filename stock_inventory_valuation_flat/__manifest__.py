# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Stock Inventory Valuation (Flat)',
    'category': 'Warehouse',
    'license': 'LGPL-3',
    'summary': '',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'version': '10.0.1.0.0',
    'description': """
Adds a menu item for non-grouped version of Inventory Valuation report.
""",
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_quant_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
