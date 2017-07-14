# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo import _, http


class Picking(models.Model):
    _inherit = 'stock.picking'

    web_url = fields.Char()

    @api.multi
    def action_send_delivery_order(self):
        for order in self:
            base_url = http.request.env['ir.config_parameter'].get_param('web.base.url', default='http://localhost:8069')
            sale_order = self.env['sale.order'].search([('name', '=', self.origin)])
            self.web_url = base_url + "/my/orders/" + str(sale_order.id)
            email_act = order.action_delivery_send()
            if email_act and email_act.get('context'):
                email_ctx = email_act['context']
                email_ctx.update(default_email_from=order.company_id.email)
                order.with_context(email_ctx).message_post_with_template(email_ctx.get('default_template_id'))
        return True

    @api.multi
    def action_delivery_send(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_set = ir_model_data.get_object_reference('stock_delivery_notification', 'email_template_edi_delivery')
            template_id = ir_model_data.get_object_reference('stock_delivery_notification', 'email_template_edi_delivery')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'stock.picking',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "stock.mail_template_data_notification_email_delivery_order"
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }