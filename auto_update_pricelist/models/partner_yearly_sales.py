# -*- coding: utf-8 -*-

from odoo import fields, models


class PartnerYearlySales(models.Model):
    _name = "partner.yearly_sales"

    partner_id = fields.Many2one(
        'res.partner',
        string = 'Partner',
    )
    start_date = fields.Date(
        string = 'Start Date',
    )
    end_date = fields.Date(
        string = 'End Date',
    )
    sales_amount = fields.Float(
        string = 'Sales Amount',
    )
