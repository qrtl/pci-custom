# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Adjustment to Account Payment Cancel",
    "summary": "",
    "description": """
* Clears move_name field of account.payment when the payment is cancelled so
that the payment can be deleted.
* See https://github.com/odoo/odoo/pull/17758
""",
    "version": "10.0.1.0.0",
    "category": "Account",
    "website": "https://www.quartile.co",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account",
    ],
}
