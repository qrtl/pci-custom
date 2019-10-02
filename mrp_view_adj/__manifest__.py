# -*- coding: utf-8 -*-
# Copyright 2018-2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Adjustments on MRP Production's views",
    "summary": "",
    "description": """
- Add remarks and location_src_id to list view and search view of MRP.
""",
    "version": "10.0.1.1.0",
    "category": "Manufacturing",
    "website": "https://www.quartile.co",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "sale_order_line_mrp_remarks",
    ],
    "data": [
        "views/mrp_production_views.xml",
    ],
}
