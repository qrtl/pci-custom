# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    additional_info1 = fields.Char('Additional Info 1')
    additional_info2 = fields.Char('Additional Info 2')
    additional_info3 = fields.Char('Additional Info 3')
