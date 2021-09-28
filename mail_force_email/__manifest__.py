# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Email Template with Force Sending",
    "version": "10.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.odoo-asia.com",
    "category": "Mail",
    "license": "LGPL-3",
    "description": """
# Add new attribute to email template that force sending emails to partner
even the Email Messages and Notifications setting is set to "Never" (i.e. you
set "Never" because you want to avoid sending internal discussion to customer
by mistake).
""",
    "depends": ["mail"],
    "data": ["views/mail_template_views.xml"],
    "installable": True,
}
