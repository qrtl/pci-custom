# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Adjust _website_price method to support multi-website',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Website',
    'license': "AGPL-3",
    'description': """
- Overwrite the price computation of website price, always apply the \
pricelist of the login-ed user if available.
""",
    'depends': [
        'website_sale',
    ],
    'data': [
    ],
    'installable': True,
}
