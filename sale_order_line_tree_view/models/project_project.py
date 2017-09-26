# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class Projectproject(models.Model):
    _inherit = "project.project"

    type = fields.Selection(
        [('stairs', 'Stairs'),
         ('handrail', 'Handrail')],
        require=True,
    )
    type2 = fields.Selection(
        [('stairs', 'Stairs'),
         ('handrail', 'Handrail')],
        require=True,
    )
    stairs = fields.Integer(
        string='Stairs (sets)',
    )
    handrail = fields.Float(
        string='Handrail (m)',
        help='Length of the handrails in meters.'
    )
    weight = fields.Float(
        string='Weight (kg)',
    )
    cad_partner_id = fields.Many2one(
        "res.partner",
        domain=[('cad_partner', '=', True)],
        string="CAD Partner",
    )
    state = fields.Selection([
        ('quotation', 'Quotation'),
        ('sales_order', 'Sales Order'),
        ('wip', 'In Progress'),
        ('invoiced', 'Invoiced'),
        ('done', 'Done')], 'Status',
        default='quotation',
        store=True
    )
    shiage = fields.Text(
        string='shiage',
        require=True,
    )
    shiage2 = fields.Text(
        string='shiage',
        require=True,
    )
