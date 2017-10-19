# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Adjustments on Product Configurator Base',
    'version': '10.0.1.0.0',
    'category': 'Generic Modules/Base',
    'summary': '',
    'author': 'Quartile Limited',
    'license': 'AGPL-3',
    'website': 'https://www.odoo-asia.com',
    'depends': [
        'product_configurator',
    ],
    "data": [
        'views/product_config_step_line_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
}
