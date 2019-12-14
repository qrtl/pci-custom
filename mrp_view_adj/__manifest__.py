# -*- coding: utf-8 -*-
# Copyright 2018-2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Adjustments on MRP Production's views",
    "summary": "",
    "description": """
- Add remarks and location_src_id to list view and search view of MRP.
- Adjustments to manufacturing order form.
""",
    "version": "10.0.1.2.0",
    "category": "Manufacturing",
    "website": "https://www.quartile.co",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale_order_line_mrp_remarks",
        "website_product_stock",
    ],
    "data": [
        "views/mrp_production_views.xml",
    ],
}
