# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Product Type Default',
    'summary': """""",
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'description': """
* Propose product type from product category
    """,
    'author': 'Rooms For (Hong Kong) Limited T/A OSCG',
    'website': 'https://www.odoo-asia.com',
    'license': 'LGPL-3',
    'depends': [
        'product',
        'stock',
    ],
    'data': [
        'views/product_category_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
