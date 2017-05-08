# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class StockConfigSettings(models.TransientModel):
    _inherit = "stock.config.settings"
    
    procurement_calc_months = fields.Integer(
        related='company_id.procurement_calc_months',
        string="No. of Months for Procurement Calc.",
        help="No. of months to consider in Product Proc. Info Update",
        required=True,
        default=6,
    )
    group_stock_procurement_plan = fields.Boolean(
        "Allow manual adjustments to needed quantities (Product Proc. Info)",
        implied_group='product_procurement_plan.group_procurement_plan',
        help="Columns will be added in Product Proc. Info screen"
    )
