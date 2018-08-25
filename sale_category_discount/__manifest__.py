# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Discount by Product Category',
    'version': '10.0.2.2.0',
    'license': 'LGPL-3',
    'category':'Sales',
    'description': """
- Adds function to apply discount based on aggregated qty per category in a
sales order.
    """,
    'author' : 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'depends': [
        'sale',
        'website_sale',
    ],
    'data':[
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
