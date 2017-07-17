# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class PartnerYearlySales(models.Model):
    _name = "partner.yearly_sales"
    _order = 'start_date desc'

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
    )
    start_date = fields.Date(
        string='Start Date',
    )
    end_date = fields.Date(
        string='End Date',
    )
    # to deprecate
    sales_amount = fields.Float(
        string='Sales Amount',
    )
    amt_computed = fields.Float(
        string = 'Computed Amount',
        readonly=True,
    )
    amt_adjust = fields.Float(
        string = 'Adjustment',
    )
    amt_total = fields.Float(
        compute='_compute_amt_total',
        store=True,
        string = 'Total Amount',
    )


    @api.multi
    @api.depends('amt_computed', 'amt_adjust')
    def _compute_amt_total(self):
        for rec in self:
            rec.amt_total = rec.amt_computed + rec.amt_adjust
