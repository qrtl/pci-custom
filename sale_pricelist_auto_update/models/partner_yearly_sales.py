# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PartnerYearlySales(models.Model):
    _name = "partner.yearly_sales"
    _order = "start_date desc"

    partner_id = fields.Many2one("res.partner", string="Partner",)
    start_date = fields.Date(string="Start Date", required=True,)
    end_date = fields.Date(string="End Date", required=True,)
    amt_computed = fields.Monetary(
        currency_field="company_currency_id", string="Computed Amount", readonly=True,
    )
    amt_adjust = fields.Monetary(
        currency_field="company_currency_id", string="Adjustment",
    )
    amt_total = fields.Monetary(
        compute="_compute_amt_total",
        store=True,
        currency_field="company_currency_id",
        string="Total Amount",
    )
    company_currency_id = fields.Many2one(
        "res.currency",
        related="partner_id.company_id.currency_id",
        string="Company Currency",
        store=True,
        readonly=True,
    )

    @api.multi
    @api.depends("amt_computed", "amt_adjust")
    def _compute_amt_total(self):
        for rec in self:
            rec.amt_total = rec.amt_computed + rec.amt_adjust
