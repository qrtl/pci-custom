# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    auto_confirm_sale_order = fields.Boolean(
        string='Auto Confirm Sales Order by Scheduled Action',
        store=True,
        default=False,
    )
    auto_confirm_threshold_date = fields.Integer(
        string='Days to Add in Threshold Date Calculation for SO Confirmation',
    )
