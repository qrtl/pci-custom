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
- Add domain_url to sales order and related email templates hence the sent \
emails will direct back to correct domain.
- Overwrite the signup url in set password and reset password email templates.
""",
    'depends': [
        'sale',
        'pr1_multi_website',
        'auth_signup',
    ],
    'data': [
        'data/mail_template_data.xml',
    ],
    'installable': True,
}
