# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = "product.category"

    analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account'
    )
