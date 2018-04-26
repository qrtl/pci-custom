# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_quotation_auto_confirm(self):
        sale_teams = self.env['crm.team'].search(
            [('auto_confirm_sale_order', '=', True)])
        for sale_team in sale_teams:
            threshold_days = sale_team.auto_confirm_threshold_date or 0
            threshold_date = (datetime.today() + timedelta(
                days=threshold_days)).strftime('%Y-%m-%d %H:%M:%S')
            pending_quotations = self.search([
                ('state', 'in', ('sent', 'draft')),
                ('team_id', '=', sale_team.id),
                '|',
                ('requested_date', '<=', threshold_date),
                ('requested_date', '=', False),
                ('commitment_date', '<=', threshold_date),
            ])
            pending_quotations.action_confirm()
        return True
