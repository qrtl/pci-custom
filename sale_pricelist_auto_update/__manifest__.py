# -*- coding: utf-8 -*-
# Copyright 2017-2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Auto Update Customer Pricelist",
    "version": "10.0.1.1.0",
    "license": "LGPL-3",
    "category": "Sales",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "depends": ["delivery", "date_range", "sale_order_line_base_amt",],
    "data": [
        "security/ir.model.access.csv",
        "views/date_range_views.xml",
        "views/partner_yearly_sales_views.xml",
        "views/product_template_views.xml",
        "views/product_pricelist_group_views.xml",
        "views/product_pricelist_views.xml",
        "wizard/update_pricelist_wizard_view.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
