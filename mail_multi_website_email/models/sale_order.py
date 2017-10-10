# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, http


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    domain_url = fields.Char()

    @api.multi
    def action_quotation_send(self):
        self.domain_url = http.request.env[
            'ir.config_parameter'].get_param('web.base.url')
        if self.partner_id:
            domain = [
                ('partner_id', '=', self.partner_id.id),
                ('active', '=', True)
            ]
            user_ids = self.env['res.users'].search(domain)
            if user_ids and user_ids[0].website_id:
                for hostheaders in user_ids[0].website_id.hostheaders:
                    self.domain_url = "https://" + hostheaders.header
        res = super(SaleOrder, self).action_quotation_send()
        return res
