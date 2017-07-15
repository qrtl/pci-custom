# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Sale Order Salesperson Filter',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Sales',
    'license': "LGPL-3",
    'description': """
* Do not propose Salesperson by default when login
* Add Boolean field to User on whether to propose the Salesperson
* Restrict invoices and sales order from selecting non-Salesperson User
""",
    'depends': [
        'account',
        'sale',
        'base',
    ],
    'data': [
        "views/account_invoice_views.xml",
        "views/sale_order_views.xml",
        "views/res_partner_views.xml",
        "views/res_users_views.xml",
    ],
    'installable': True,
}
