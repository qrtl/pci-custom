# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Invoice Line Views",
    "summary": "Adds menu items for invoice liines",
    "description": """
* Add menu items Customer Invoice Lines and Vendor Bill Lines
* Captures exchange rates as of the invoice dates and shows the base currency
amounts in the output.
""",
    "version": "10.0.1.0.0",
    "category": "Account",
    "website": "https://www.odoo-asia.com/",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["account"],
    "data": ["views/account_invoice_views.xml"],
}
