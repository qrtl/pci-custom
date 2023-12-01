# -*- coding: utf-8 -*-
# Copyright 2018-2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Orders Invoice Automation",
    "summary": "",
    "description": """
This module provides automation of invoice operations for online sales order.
- Add Boolean field to crm.team to determine whether the invoice will be
automatically created and validated.
- Auto creating and validating invoice when the delivery order of sales
order is confirmed
- Add a scheduled action to perform the operation.
""",
    "version": "10.0.1.0.1",
    "category": "Account",
    "website": "https://www.quartile.co",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account",
        "sale_stock",
    ],
    "data": [
        "views/crm_team_views.xml",
        "views/sale_order_views.xml",
    ],
}
