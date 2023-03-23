# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgp1).
{
    'name': 'View Adjustments on Website Sale',
    'version': '10.0.1.0.0',
    'category': 'Website',
    'summary': '',
    'description': """
* Adjust shopping cart view
* Adjust product page view
    """,
    'author': 'Quartile Limited',
    'license': 'LGPL-3',
    'website': 'https://www.quartile.co',
    'depends': [
        'website_sale',
    ],
    'data': [
        'views/templates.xml'
    ],
    'installable': True,
}
