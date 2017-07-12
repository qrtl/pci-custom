# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Adjustments on Accounting Views',
    'summary':"""""",
    'version': '10.0.1.1.0',
    'category': 'Accounting',
    'description': """
    """,
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'license': 'LGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_invoice_views.xml',
        'views/report_invoice.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
