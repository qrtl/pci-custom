# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Adjustments on Accounting Views',
    'summary':"""""",
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'description': """
    """,
    'author': 'Rooms For (Hong Kong) Limited T/A OSCG',
    'website': 'https://www.odoo-asia.com',
    'license': 'LGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'views/account_invoice_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
