# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ShipmentScheduleReportWizard(models.TransientModel):
    _name = "shipment.schedule.report.wizard"
    _description = 'Shipment Schedule Report Wizard'

    threshold_date = fields.Date(
        string='Threshold Date',
        default=fields.Date.context_today,
        required=True,
    )
    limit_locs = fields.Boolean(
        string='Limit Locations',
        default=True,
        help="Only consider stock in locations that are meant to be available "
             "for customers. If unselected, consider all the internal "
             "locations",
    )
    website_published = fields.Boolean(
        string='Only Show Products Published on Website',
        default=True,
        help="Enable option to filter out the products that are unpublished "
             "on website. Otherwise, both published and unpublished product "
             "will be exported to the report",
    )
    categ_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category',
    )

    @api.multi
    def action_export_xlsx(self):
        self.ensure_one()
        model = self.env['shipment.schedule.report']
        report = model.create(self._prepare_report_xlsx())
        return report.print_report()

    def _prepare_report_xlsx(self):
        self.ensure_one()
        return {
            'threshold_date': self.threshold_date,
            'limit_locs': self.limit_locs,
            'website_published': self.website_published,
            'categ_id': self.categ_id.id or False,
            'categ_name': self.categ_id.display_name or False
        }
