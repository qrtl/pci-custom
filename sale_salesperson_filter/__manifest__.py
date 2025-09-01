# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Sale Order Salesperson Filter',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Sales',
    'license': "LGPL-3",
    'description': """
* Add Salesperson attribute to User
* Only User with Salesperson attribute could be assigned as the Salesperson
  of Customer
* Restrict selection on Salesperon in Sales Order and Invoices
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
