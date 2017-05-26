# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgp1).
{
    'name': 'Enhanced Stock Level Forecast Report',
    'category': 'Warehouse',
    'license': 'LGPL-3',
    'summary': 'Enhanced Stock Level Forecast Report',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com/',
    'version': '10.0.1.0.0',
    'description': """
Added Product Category and Can Be Sold filters for Stock Level
Forecast Report.
""",
    'depends': ['stock'],
    'data': [
        'report/report_stock_forecast.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
