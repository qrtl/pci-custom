# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': "Stock Inventory Product Type",
    'version': "10.0.1.0.1",
    'author': "Rooms For (Hong Kong) Limited T/A OSCG",
    'website': "https://www.odoo-asia.com/",
    'category': "Stock",
    'license': "LGPL-3",
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_quant_views.xml',
    ],
    "application": False,
    "installable": True,
}
