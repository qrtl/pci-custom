# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Line View",
    "summary": "Adds an menu item for Purchase Order Lines",
    "version": "10.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Purchases",
    "depends": [
        "purchase_open_qty",
        "purchase_stock_picking_return_invoicing",
    ],
    "data": [
        'views/purchase_line_views.xml',
    ],
    "license": "AGPL-3",
    "installable": True,
}
