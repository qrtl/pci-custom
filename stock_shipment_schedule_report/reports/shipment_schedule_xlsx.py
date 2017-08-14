# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from openerp import api, models, fields, _
from openerp.addons.abstract_report_xlsx.reports \
    import stock_abstract_report_xlsx
from openerp.report import report_sxw


class ShipmentScheduleXlsx(stock_abstract_report_xlsx.StockAbstractReportXlsx):

    def __init__(self, name, table, rml=False, parser=False, header=True,
                 store=False):
        super(ShipmentScheduleXlsx, self).__init__(
            name, table, rml, parser, header, store)

    def _get_report_name(self):
        return _('Shipment Schedule Report')

    def _get_report_columns(self, report):
        return {
            0: {
                'header': _('Product'),
                'field': 'product_name',
                'width': 30
            },
            1: {
                'header': _('Product Category'),
                'field': 'categ_name',
                'width': 32
            },
            2: {
                'header': _('Inv. on Hand'),
                'field': 'bal1',
                'type': 'number',
                'width': 8
            },
            3: {
                'header': _('Receipt'),
                'field': 'in2',
                'type': 'number',
                'width': 8
            },
            4: {
                'header': _('Shipt. on Hold'),
                'field': 'out0',
                'type': 'number',
                'width': 8
            },
            5: {
                'header': _('Shipt.'),
                'field': 'out1',
                'type': 'number',
                'width': 8
            },
            6: {
                'header': _('Balance'),
                'field': 'bal2',
                'type': 'number',
                'width': 8
            },
            7: {
                'header': _('Receipt'),
                'field': 'in3',
                'type': 'number',
                'width': 8
            },
            8: {
                'header': _('Shipt.'),
                'field': 'out3',
                'type': 'number',
                'width': 8
            },
            9: {
                'header': _('Balance'),
                'field': 'bal3',
                'type': 'number',
                'width': 8
            },
            10: {
                'header': _('Receipt'),
                'field': 'in4',
                'type': 'number',
                'width': 8
            },
            11: {
                'header': _('Shipt.'),
                'field': 'out4',
                'type': 'number',
                'width': 8
            },
            12: {
                'header': _('Balance'),
                'field': 'bal4',
                'type': 'number',
                'width': 8
            },
            13: {
                'header': _('Receipt'),
                'field': 'in5',
                'type': 'number',
                'width': 8
            },
            14: {
                'header': _('Shipt.'),
                'field': 'out5',
                'type': 'number',
                'width': 8
            },
            15: {
                'header': _('Balance'),
                'field': 'bal5',
                'type': 'number',
                'width': 8
            },
            16: {
                'header': _('Receipt'),
                'field': 'in6',
                'type': 'number',
                'width': 8
            },
            17: {
                'header': _('Shipt.'),
                'field': 'out6',
                'type': 'number',
                'width': 8
            },
            18: {
                'header': _('Balance'),
                'field': 'bal6',
                'type': 'number',
                'width': 8
            },
        }

    def _get_report_filters(self, report):
        report_date = fields.Datetime.to_string(
            fields.Datetime.context_timestamp(
                report, datetime.now()
            )
        )
        return [
            [_('Report Date'), report_date],
            [_('Threshold Date'), report.threshold_date],
            [_('Product Category'), report.categ_name or 'All Categories'],
        ]

    def _get_col_count_filter_name(self):
        return 1

    def _get_col_count_filter_value(self):
        return 1

    def _get_periods(self, report):
        periods = {
            3: {
                'header': report.p2,
                'col_plus': 3
            },
            7: {
                'header': report.p3,
                'col_plus': 2
            },
            10: {
                'header': report.p4,
                'col_plus': 2
            },
            13: {
                'header': report.p5,
                'col_plus': 2
            },
            16: {
                'header': report.p6,
                'col_plus': 2
            }
        }
        return periods

    def _generate_report_content(self, workbook, report):
        periods = self._get_periods(report)
        self.write_header_periods(periods)
        self.write_array_header()
        for line in report.line_ids:
            self.write_line(line)

ShipmentScheduleXlsx(
    'report.stock_shipment_schedule_report.shipment_schedule_report',
    'shipment.schedule.report',
    parser=report_sxw.rml_parse
)
