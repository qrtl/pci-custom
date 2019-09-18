# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Update Sales Order\'s Invoice Policy',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Stock',
    'license': "AGPL-3",
    'description': "",
    'depends': [
        'website_order_invoice_automation',
    ],
    'data': [
        'views/sale_order_views.xml',
        'wizards/sale_order_invoice_policy_report_wizard_views.xml',
    ],
    'installable': True,
}
