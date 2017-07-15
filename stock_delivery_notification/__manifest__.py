# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Delivery Order Notification',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Stock',
    'license': "LGPL-3",
    'description': """
# Send email to customer when delivery order is done
""",
    'depends': [
        'sale_stock',
        'mail',
        'mail_force_email',
    ],
    'data': [
        'data/mail_template_data.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
}
