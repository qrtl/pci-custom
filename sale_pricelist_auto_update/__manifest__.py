# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Auto Update Customer Pricelist',
    'summary': 'Auto Update Customer Pricelist',
    'version': '10.0.1.0.0',
    'license': 'LGPL-3',
    'category':'Sales',
    'description': """
# Module will updates pricelist on customer based on yearly purchase amount.
    """,
    'author' : 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'depends': [
        'delivery',
    ],
    'data':[
        'security/ir.model.access.csv',
        'data/policy_pricelist_reminder_data.xml',
        'wizard/update_pricelist_wizard_view.xml',
        'views/product_pricelist_policy_views.xml',
        'views/res_partner_views.xml',
        'views/product_pricelist_views.xml',
    ],
    'installable': True,
    'application': False,
}
