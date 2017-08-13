# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Shipment Schedule Report",
    "summary": "",
    "version": "10.0.1.0.0",
    "category": "Reporting",
    "website": "https://www.odoo-asia.com/",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "sale_order_dates_ext",
        "sale_stock",
        "abstract_report_xlsx",
    ],
    "data": [
        "wizards/shipment_schedule_report_wizard_view.xml",
        "reports.xml",
    ],
}
