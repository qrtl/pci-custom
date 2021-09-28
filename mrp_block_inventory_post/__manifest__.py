# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "MRP Block Inventory Post",
    "summary": "",
    "description": """
- Adds checking to prevent inventory post for manufacturig order when there
is an unreserved stock move for components.
""",
    "version": "10.0.1.1.0",
    "category": "Manufacturing",
    "website": "https://www.quartile.co",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["mrp"],
}
