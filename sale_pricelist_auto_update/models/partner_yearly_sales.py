# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class PartnerYearlySales(models.Model):
    _name = "partner.yearly_sales"
    _order = 'start_date desc'

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
