# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Account Analytic Default Product Category",
    "summary": """""",
    "version": "10.0.1.0.0",
    "category": "Accounting & Finance",
    "description": """
* Add 'Analytic Account' to Product Category
* If no corresponding Analytic Defaults, automatically propose Analytic Account of Product Category on Invoice lines
* Do not propose it on Purchase Order lines
    """,
    "author": "Rooms For (Hong Kong) Limited T/A OSCG",
    "website": "https://www.odoo-asia.com",
    "license": "LGPL-3",
    "depends": ["account", "account_analytic_default",],
    "data": ["views/product_category_views.xml",],
    "installable": True,
    "application": False,
    "auto_install": False,
}
