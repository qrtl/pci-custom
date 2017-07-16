# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    sale_threshold_amt = fields.Monetary(
        string='Sale Threshold Amount',
        currency_field='company_currency_id',
        copy=False,
    )
    pricelist_group_id = fields.Many2one(
        comodel_name='product.pricelist.group',
        string='Pricelist Group',
        copy=False,
    )
    company_currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        string="Company Currency",
        readonly=True,
        store=True
    )
