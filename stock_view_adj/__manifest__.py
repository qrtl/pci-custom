# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Stock View Adjust',
    'version': '10.0.1.1.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Stock',
    'license': "LGPL-3",
    'description': """
- Stock Inventory View : Display the validation button when operated by Manager and Users.
- Stock Picking View : Disable Force Availability.
    """,
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_inventory_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
}
