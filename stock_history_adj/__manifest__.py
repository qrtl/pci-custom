# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Adjustments on Stock History",
    "version": "10.0.1.0.1",
    "description": """
* Add product_type in the output to filter and show stockable products only
    """,
    "author": "Rooms For (Hong Kong) Limited T/A OSCG",
    "website": "https://www.odoo-asia.com/",
    "category": "Stock",
    "license": "LGPL-3",
    "depends": ["stock_account"],
    "data": ["report/stock_history_views.xml"],
    "application": False,
    "installable": True,
}
