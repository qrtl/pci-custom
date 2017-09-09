# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, http


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    web_url = fields.Char()
    # to keep the SO number to show on email because 'origin' field cannot be
    # relied on in case of re-delivery after return
    origin_sale = fields.Char()

    date_done_ctx = fields.Char(
        compute='_get_date_done_ctx',
        store=True,
    )

    @api.multi
    @api.depends('date_done')
    def _get_date_done_ctx(self):
        for picking in self:
            if picking.date_done:
                datetime_done_ctx = fields.Datetime.context_timestamp(
                    picking, fields.Datetime.from_string(picking.date_done)
                )
                picking.date_done_ctx = datetime_done_ctx.strftime(
                    "%Y-%m-%d %H:%M:%S %Z")

    @api.multi
    def action_send_delivery_order(self):
        # send notification email for online orders only
        self.ensure_one()
        if self.picking_type_id.code == "outgoing" and self.group_id:
            so_rec = self.env['sale.order'].search(
                [('procurement_group_id', '=', self.group_id.id)])
            if so_rec and so_rec[0].team_id and so_rec[0].team_id.id == \
                    self.env.ref('sales_team.salesteam_website_sales').id:
                self.origin_sale = so_rec[0].name
                base_url = http.request.env['ir.config_parameter'].get_param(
                    'web.base.url')
                self.web_url = base_url + "/my/orders/" + str(so_rec[0].id)
                email_act = self.action_delivery_send()
                if email_act and email_act.get('context'):
                    email_ctx = email_act['context']
                    self.with_context(email_ctx).message_post_with_template(
                        email_ctx.get('default_template_id'))
        return True

    @api.multi
    def action_delivery_send(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference(
                'stock_delivery_notification',
                'email_template_edi_delivery')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(
                'mail',
                'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'stock.picking',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout':
                "stock.mail_template_data_notification_email_delivery_order"
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

    @api.multi
    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        if 'date_done' in vals:
            for pick in self:
                pick.action_send_delivery_order()
        return res
