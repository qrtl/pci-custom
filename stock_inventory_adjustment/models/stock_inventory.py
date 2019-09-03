# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    note = fields.Text(
        string='Note',
        store=True,
    )