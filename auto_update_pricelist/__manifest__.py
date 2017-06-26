# -*- coding: utf-8 -*-
# Part of Rooms For (Hong Kong) Ltd T/A OSCG. See LICENSE file for full copyright and licensing details.

{
    'name': 'Auto Update Customer Pricelist',
    'summary': 'Auto Update Customer Pricelist',
    'version': '10.0.0.0.1',
    'license': 'AGPL-3',
    'category':'Sales',
    'description': """
Module will updates pricelist on customer based on yearly purchase amount.
    """,
    'author' : 'Rooms For (Hong Kong) Ltd T/A OSCG',
    'website': 'http://www.openerp-asia.net',
    'depends': [
        'delivery',
    ],
    'data':[
        'security/ir.model.access.csv',
        'data/policy_pricelist_reminder_data.xml',
        'wizard/update_pricelist_wizard_view.xml',
        'views/product_pricelist_policy.xml',
        'views/partner.xml',
        'views/product_pricelist_views.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
