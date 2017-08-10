# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, models, fields


class ShipmentScheduleReportWizard(models.TransientModel):
    _name = "shipment.schedule.report.wizard"
    _description = 'Shipment Schedule Report Wizard'

    threshold_date = fields.Date(
        string='Threshold Date',
        default=fields.Date.context_today,
    )
    categ_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category',
    )


    @api.multi
    def action_export_xlsx(self):
        self.ensure_one()
        model = self.env['schedule.report']
        report = model.create(self._prepare_report_xlsx())
        return report.print_report()

    def _prepare_report_xlsx(self):
        self.ensure_one()
        return {
            'threshold_date': self.threshold_date,
            'category_id': self.categ_id or False,
        }


# from openerp.osv import fields, osv
# import logging
# _logger = logging.getLogger(__name__)
#
#
# class stock_shipment_schedule(osv.osv_memory):
#     _name = "stock.shipment.schedule"
#     _description = "Shipment Schedule Report"
#     _columns = {
#         'threshold_date': fields.date('Threshold Date'),
#         'category_id': fields.many2one('product.category', 'Product Category'),
#     }
#
#     _defaults = {
#         'threshold_date': fields.date.context_today,
#     }
#
#     def show_schedule(self, cr, uid, ids, context=None):
#         data = {}
#         for params in self.browse(cr, uid, ids, context=context):
#             data['threshold_date'] = params.threshold_date
#             data['category_id'] = params.category_id.id
#
#         return {
#             'type':'ir.actions.report.xml',
#             'datas':data,
#             'report_name':'shipment_schedule_report',
#         }
