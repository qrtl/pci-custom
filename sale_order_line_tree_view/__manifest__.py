# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Sales Order Line Tree View',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Sales',
    'license': "LGPL-3",
    'description': """
* Add tree view to Sales Order Lines
""",
    'depends': [
        'sale',
        'sale_order_lot_selection',
    ],
    'data': [
        "views/sale_order_line_views.xml",
    ],
    'installable': True,
}
