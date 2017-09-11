# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Delivery Order Notification',
    'version': '10.0.1.1.3',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Stock',
    'license': "LGPL-3",
    'description': """
Send email to the customer for online orders when delivery is done.
""",
    'depends': [
        'mail_force_email',
        'sale_stock',
        'website_portal_sale',
        'shipstation_globalteckz',
    ],
    'data': [
        'data/mail_template_data.xml',
    ],
    'installable': True,
}
