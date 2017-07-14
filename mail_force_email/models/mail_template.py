# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    force_email = fields.Boolean(
        string="Force Sending Email",
        default=False,
    )
