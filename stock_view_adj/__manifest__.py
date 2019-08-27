# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Disable Force Availability',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Stock',
    'license': "LGPL-3",
    'description': "",
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_inventory_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
}
