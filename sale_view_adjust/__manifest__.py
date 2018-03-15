# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Adjustments on Sales Views',
    'summary':"""""",
    'version': '10.0.1.2.1',
    'category': 'Sales',
    'description': """
    """,
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'license': 'LGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'report/sale_report_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
