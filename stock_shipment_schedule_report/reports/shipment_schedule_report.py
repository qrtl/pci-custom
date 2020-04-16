# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ShipmentScheduleReport(models.TransientModel):
    # class fields are defined here
    _name = 'shipment.schedule.report'

    threshold_date = fields.Date()
    limit_locs = fields.Boolean()
    website_published = fields.Boolean()
    categ_name = fields.Char()
    p2 = fields.Char()
    p3 = fields.Char()
    p4 = fields.Char()
    p5 = fields.Char()
    p6 = fields.Char()

    # # Data fields, used to browse report data
    categ_id = fields.Many2one(
        comodel_name='product.category',
    )
    line_ids = fields.One2many(
        comodel_name='shipment.schedule.report.line',
        inverse_name='report_id'
    )
