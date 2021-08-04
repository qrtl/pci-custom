# -*- coding: utf-8 -*-
# © 2017 Pierre Faniel
# © 2017 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'

    import_limit = fields.Integer('Serial Number Import Limit',
                                  default=lambda self: self.get_import_limit())

    def get_import_limit(self):
        return self.env['ir.config_parameter'].get_param(
            'stock.serial.import.limit', 1000)

    def set_import_limit(self):
        self.env['ir.config_parameter'].set_param('stock.serial.import.limit',
                                                  self.import_limit)
