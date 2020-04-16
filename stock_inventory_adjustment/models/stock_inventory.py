# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    note = fields.Text(
        string='Note',
    )
