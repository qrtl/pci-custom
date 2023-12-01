# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    # override the standard method.
    # if force_email is enabled in used template, send email to partner
    # regardless of partner's notify_email setting
    @api.multi
    def _notify(self,
                message,
                force_send=False,
                send_after_commit=True,
                user_signature=True):
        message_sudo = message.sudo()
        email_channels = message.channel_ids.filtered(
            lambda channel: channel.email_send
        )
        # adjust start (QTL)
        domain = [
            '|',
            ('id', 'in', self.ids),
            ('channel_ids', 'in', email_channels.ids),
            ('email', '!=',
             message_sudo.author_id
             and message_sudo.author_id.email
             or message.email_from)
        ]
        layout = self._context.get('custom_layout', False)
        if not (layout and self.env.ref(layout).force_email):
            domain.append(('notify_email', '!=', 'none'))
        self.sudo().search(domain)._notify_by_email(
            message, force_send=force_send,
            send_after_commit=send_after_commit,
            user_signature=user_signature
        )
        # adjust end (QTL)
        self._notify_by_chat(message)
        return True
