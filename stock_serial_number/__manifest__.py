# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Stock Serial Number',
    'version': '10.0.1.2.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Stock',
    'license': "LGPL-3",
    'description': "",
    'depends': [
        'sale',
        'stock',
        'sale_order_lot_selection',
        'account_invoice_line_view',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_model_views.xml',
        'views/stock_body_views.xml',
        'views/stock_neck_views.xml',
        'views/stock_pickguard_views.xml',
        'views/stock_shop_views.xml',
        'views/stock_production_lot_views.xml',
        'views/account_invoice_views.xml',
        'views/stock_move_views.xml',
    ],
    'installable': True,
}
