# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Serial Number for Sales Order Line",
    "version": "10.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Sales",
    "license": "LGPL-3",
    "description": """
Add "Serial Number" field to sales order line, the field will be passed to
invoice and manufacturing order.
""",
    "depends": [
        "mrp",
        "sale_order_lot_selection",
        "sale_order_line_tree_view",
        "stock_serial_number",
    ],
    "data": [
        "report/report_invoice.xml",
        "views/account_invoice_line_views.xml",
        "views/account_invoice_views.xml",
        "views/sale_order_line_views.xml",
        "views/sale_order_views.xml",
        "views/mrp_production_views.xml",
    ],
    "installable": True,
}
