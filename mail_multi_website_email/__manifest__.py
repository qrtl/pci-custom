# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Support Multi-Website feature in email templates',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Mail',
    'license': "LGPL-3",
    'description': """
- Override the get_access_action in Sale Order to add the domain url to the \
confirmation email.
- Overwrite the signup url in set password and reset password email templates.
""",
    'depends': [
        'sale',
        'pr1_multi_website',
        'auth_signup',
        'website_portal_sale',
    ],
    'data': [
    ],
    'installable': True,
}
