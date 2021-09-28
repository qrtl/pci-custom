# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Manufacturing Order Change Source Locations",
    "summary": "",
    "description": """
""",
    "version": "10.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://www.quartile.co",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["mrp"],
    "data": [
        "wizard/change_source_location_wizard_views.xml",
        "views/mrp_production_views.xml",
    ],
}
