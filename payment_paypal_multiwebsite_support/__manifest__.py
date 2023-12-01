# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Extend PayPal Acquirer to support multi-website',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Accounting',
    'license': "AGPL-3",
    'description': """
- Override the paypal_form_generate_values in payment_paypal module to \
modify the return url sent to PayPal
""",
    'depends': [
        'payment_paypal',
    ],
    'data': [
    ],
    'installable': True,
}
