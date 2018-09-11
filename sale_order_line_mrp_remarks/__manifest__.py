# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Remarks for Manufacturing Order",
    "summary": "",
    "description": """
- Adds remark field in sales order line.
- Pass the remark field to corresponding manufacturing orders.
""",
    "version": "10.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://www.quartile.co",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "sale",
        "mrp",
    ],
    "data": [
        "views/sale_order_views.xml",
        "views/mrp_production_views.xml",
    ],
}
