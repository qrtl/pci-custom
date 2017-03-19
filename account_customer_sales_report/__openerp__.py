# -*- coding: utf-8 -*-
# Copyright 2015-2017 Rooms For (Hong Kong) Limited T/A OSCG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Customer Sales Report',
    'version': '7.0.1.0.1',
    'category': "Report",
    'summary': 'Adds a report function to print sales by customer',
    'description': """
 * Adds a boolean field 'Customer Sales Report' in account definition screen.
The field is expected to be selected for sales accounts that should be considered in amount calculation.
 * Adds a menu item 'Customer Sales Report' which generates a sales report by customer by period 
     """,
    'author': 'Rooms For (Hong Kong) T/A OSCG',
    'depends': ['base','account','report_aeroo_ooo','report_aeroo'],
    'init_xml': [],
    'update_xml': [
        'wizard/customer_sales_wizard.xml',
        'customer_sales.xml',
        'account.xml',
    ],
   
    'demo_xml': [],
    'installable': True,
    'active': False,
}
