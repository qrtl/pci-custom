# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Product Procurement Planning",
    "version": "10.0.1.0.1",
    "category": "Product",
    "summary": "",
    "description": """
Main Features
-------------
1. Adds procurement related fields to product.
2. Adds a menu item to open a wizard to run updates on procurement related fields in product.
3. Adds a menu item to open a product tree view tailored to show procurement related info.
     """,
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "depends": ["purchase", "mrp"],
    "data": [
        "security/product_security.xml",
        "views/stock_config_settings_views.xml",
        "views/product_product_views.xml",
        "wizard/product_procurement_view.xml",
    ],
    "installable": True,
}
