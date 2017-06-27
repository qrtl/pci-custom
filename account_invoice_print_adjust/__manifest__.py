# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Adjustments on Printing Account Invoice',
    'summary':"""""",
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'description': """
    """,
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'sale',
    ],
    'data': [
        'report/account_invoice_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
