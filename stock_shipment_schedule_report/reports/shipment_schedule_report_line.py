# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ScheduleReportLine(models.TransientModel):
    _name = 'shipment.schedule.report.line'

    report_id = fields.Many2one(
        comodel_name='shipment.schedule.report',
        ondelete='cascade',
        index=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        index=True,
    )
    categ_id = fields.Many2one(
        comodel_name='product.category',
    )

    product_name = fields.Char()
    categ_name = fields.Char()
    bal1 = fields.Float()
    in0 = fields.Float()
    out0 = fields.Float()
    in1 = fields.Float()
    out1 = fields.Float()
    in2 = fields.Float()  # first period in output
    out2 = fields.Float()
    bal2 = fields.Float()
    in3 = fields.Float()  # second period in output
    out3 = fields.Float()
    bal3 = fields.Float()
    in4 = fields.Float()  # third period in output
    out4 = fields.Float()
    bal4 = fields.Float()
    in5 = fields.Float()  # fourth period in output
    out5 = fields.Float()
    bal5 = fields.Float()
    in6 = fields.Float()  # fifth period in output
    out6 = fields.Float()
    bal6 = fields.Float()
