# -*- coding: utf-8 -*-
# Copyright 2018-2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Sale Order Line Remarks",
    "summary": "",
    "version": "10.0.1.1.0",
    "category": "Sales",
    "website": "https://www.quartile.co",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["sale", "mrp"],
    "data": [
        "report/invoice_report_templates.xml",
        "report/sale_report_templates.xml",
        "views/account_invoice_views.xml",
        "views/sale_order_views.xml",
        "views/mrp_production_views.xml",
    ],
}
