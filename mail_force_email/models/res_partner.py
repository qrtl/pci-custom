# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _notify(self, message, force_send=False, send_after_commit=True, user_signature=True):
        # TDE TODO: model-dependant ? (like customer -> always email ?)
        message_sudo = message.sudo()
        email_channels = message.channel_ids.filtered(lambda channel: channel.email_send)
        force_email = False
        if self._context.get('custom_layout', False):
            base_template = self.env.ref(self._context['custom_layout'], raise_if_not_found=False)
            force_email = base_template.force_email
        if force_email:
            self.sudo().search([
                '|',
                ('id', 'in', self.ids),
                ('channel_ids', 'in', email_channels.ids),
                ('email', '!=', message_sudo.author_id and message_sudo.author_id.email or message.email_from)
            ])._notify_by_email(message, force_send=force_send,
                                send_after_commit=send_after_commit,
                                user_signature=user_signature)
        else:
            self.sudo().search([
                '|',
                ('id', 'in', self.ids),
                ('channel_ids', 'in', email_channels.ids),
                ('email', '!=', message_sudo.author_id and message_sudo.author_id.email or message.email_from),
                ('notify_email', '!=', 'none')
            ])._notify_by_email(message, force_send=force_send,
                                send_after_commit=send_after_commit,
                                user_signature=user_signature)
        self._notify_by_chat(message)
        return True
