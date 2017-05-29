# -*- coding: utf-8 -*-
# Part of Rooms For (Hong Kong) Ltd T/A OSCG. See LICENSE file for full copyright and licensing details.

{
    'name': 'Enhanced Stock Level Forecast Report',
    'category': 'Warehouse',
    'license': 'AGPL-3',
    'summary': 'Enhanced Stock Level Forecast Report',
    'author': 'Rooms For (Hong Kong) Ltd T/A OSCG',
    'website': 'http://www.openerp-asia.net',
    'version': '10.0.0.0.1',
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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
