# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Email template with Force Sending',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Mail',
    'license': "LGPL-3",
    'description': """
# Add new attribute to email template that force sending emails to user
even the Email Messages and Notifications setting is set to "Never"
""",
    'depends': [
        'mail',
    ],
    'data': [
        'views/mail_template_views.xml',
    ],
    'installable': True,
}
