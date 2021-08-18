# -*- coding: utf-8 -*-
# Copyright 2017-2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Product Delivery Method",
    "summary": "Website Product Delivery Method",
    "version": "10.0.1.1.0",
    "license": "AGPL-3",
    "category": "Sales",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "depends": ["website_sale_delivery",],
    "data": [
        "data/customer_group_data.xml",
        "security/ir.model.access.csv",
        "views/customer_group_view.xml",
        "views/res_partner_view.xml",
        "views/delivery_carrier_view.xml",
        "views/product_category_view.xml",
    ],
    "installable": True,
}
