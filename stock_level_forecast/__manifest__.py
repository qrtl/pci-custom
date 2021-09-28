# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Stock Level Forecast Report",
    "category": "Warehouse",
    "license": "LGPL-3",
    "summary": "Enhanced Stock Level Forecast Report",
    "author": "Quartile Limited",
    "website": "https://www.odoo-asia.com",
    "version": "10.0.1.0.0",
    "description": """
Adds Can Be Sold and Product Category filters to Stock Level Forecast Report.
""",
    "depends": ["stock"],
    "data": ["report/report_stock_forecast.xml"],
    "installable": True,
    "auto_install": False,
}
