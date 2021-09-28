# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Prohibit Cancellation of Delivered Sales Orders",
    "version": "10.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.odoo-asia.com",
    "category": "Sales",
    "license": "LGPL-3",
    "description": """
When user tries to cancel a delivered sales order, there will be a pop
message and prevent user from performing the action.
""",
    "depends": ["sale_stock"],
    "data": [],
    "installable": True,
}
