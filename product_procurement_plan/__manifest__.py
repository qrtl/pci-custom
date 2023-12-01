# -*- coding: utf-8 -*-
# Copyright 2017-2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Product Procurement Planning',
    'version': '10.0.1.2.0',
    'category': 'Product',
    "author": "Quartile Limited",
    'website': 'https://www.quartile.co',
    "license": "AGPL-3",
    "depends": [
        "purchase",
        "mrp",
        "sale",
    ],
    'data': [
        'security/product_security.xml',
        'views/stock_config_settings_views.xml',
        'views/product_product_views.xml',
        'wizard/product_procurement_views.xml',
    ],
    'installable': True,
}
