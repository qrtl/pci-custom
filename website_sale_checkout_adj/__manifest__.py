# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgp1).
{
    'name': 'View Adjustments on Website Sale',
    'version': '10.0.0.0.0',
    'category': 'Website',
    'summary': '',
    'description': """
Show a message to prompt inputting the fullname below the name field.
And make the zip_code field mandatory.
    """,
    'author': 'Quartile Limited',
    'license': 'LGPL-3',
    'website': 'https://www.odoo-asia.com/',
    'depends': [
        'website_sale',
    ],
    'data': [
        'views/website_sale.xml'
    ],
    'installable': True,
}
