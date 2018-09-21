# -*- coding: utf-8 -*-
# © 2017 Pierre Faniel
# © 2017 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import csv
from odoo import _, api, exceptions, fields, models


class SerialNumberMethodWizard(models.TransientModel):
    _name = 'serial.number.method.wizard'

    @api.multi
    def manual_method(self):
        """
        :return: The original action to fill the serial numbers manually one by
         one
        """
        self.ensure_one()
        operation = self.env['stock.pack.operation'].browse(
            self.env.context.get('active_ids', []))
        return operation.action_split_lots()

    @api.multi
    def import_method(self):
        """
        :return: Action to the wizard to import serial numbers
        """
        self.ensure_one()
        import_wizard = \
            'stock_import_serial_numbers.serial_number_import_wizard_form'
        return {
            'name': _('Import Serial Numbers'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'serial.number.import.wizard',
            'view_id': self.env.ref(import_wizard).id,
            'target': 'new',
            'context': self.env.context,
        }


class SerialNumberImportWizard(models.TransientModel):
    _name = 'serial.number.import.wizard'

    import_lines = fields.Text('Serial Numbers', required=True)
    import_limit = fields.Integer('Import Limit',
                                  default=lambda self: self.get_import_limit())

    def get_import_limit(self):
        """
        :return: The global amount parameter of serial numbers that can be
        imported at once
        """
        return self.env['ir.config_parameter'].get_param(
            'stock.serial.import.limit', 1000)

    @api.multi
    def import_serial_numbers(self):
        """
        Reads all the line in the text area and tries to transform each line
        into a serial number
        """
        self.ensure_one()
        # Avoid blank lines by removing spaces
        self.import_lines = self.import_lines.replace(' ', '')
        lines = self.import_lines.split('\n')
        # Filter blank lines out
        lines = filter(lambda line: line != '', lines)
        # Avoid duplicates
        lines = list(set(lines))
        amount_of_lines = len(lines)
        if amount_of_lines > self.import_limit:
            raise exceptions.Warning(
                'Maximum %d rows allowed' % self.import_limit)

        lines_too_long = [line for line in lines if len(line) > 64]

        if lines_too_long:
            raise exceptions.Warning(
                'The following serial numbers are longer than 64 '
                'characters:\n%s' % '\n'.join(lines_too_long))

        operation = self.env['stock.pack.operation'].browse(
            self.env.context.get('active_ids', []))
        if operation.qty_done + amount_of_lines > operation.product_qty:
            exceptions.Warning(
                'There are too many lines for the lot (%d lines expected, %d '
                'lines received)' %
                (operation.product_qty - operation.qty_done, amount_of_lines))
        existing_lines, serials = [], []
        OperationLot = self.env['stock.pack.operation.lot']
        ProductionLot = self.env['stock.production.lot']
        for line in lines:
            if operation.pack_lot_ids.filtered(
                    lambda lot: lot.lot_name == line):
                existing_lines.append(line)
                continue
            production_lot = ProductionLot.create({
                'name': line,
                'product_id': operation.product_id.id,
            })
            OperationLot.create({
                'qty': 1,
                'lot_name': line,
                'operation_id': operation.id,
                'lot_id': production_lot.id,
            })
        if existing_lines:
            raise exceptions.Warning('The following serial numbers are already'
                                     ' in the system:\n%s' %
                                     '\n'.join(existing_lines))
        operation.write({'qty_done': operation.qty_done + amount_of_lines})
