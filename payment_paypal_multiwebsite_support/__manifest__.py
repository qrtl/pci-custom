# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Provide mutli-website feature to PayPal Acquirer',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Accounting',
    'license': "AGPL-3",
    'description': """
- Override the paypal_form_generate_values in payment_paypal module to \
modify the return url sent to PayPal
""",
    'depends': [
        'payment_paypal',
        'pr1_multi_website',
    ],
    'data': [
    ],
    'installable': True,
}
