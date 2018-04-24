# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_quotation_auto_confirm(self):
        threshold_date = (datetime.today() + timedelta(days=7)).strftime(
            '%Y-%m-%d %H:%M:%S')
        pending_quotations = self.search([
            ('state', 'in', ('sent', 'draft')),
            ('team_id', '=', self.env.ref(
                'sales_team.team_sales_department').id),
            '|',
            ('requested_date', '<=', threshold_date),
            ('requested_date', '=', False),
            ('commitment_date', '<=', threshold_date),
        ])
        pending_quotations.action_confirm()
        return True
