# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

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
                'width': 20
            },
            1: {
                'header': _('Product Category'),
                'field': 'categ_name',
                'width': 30
            },
            2: {
                'header': _('Inventory on Hand'),
                'field': 'bal1',
                'type': 'number',
                'width': 9
            },
            3: {
                'header': _('Receipt'),
                'field': 'in2',
                'type': 'number',
                'width': 9
            },
            4: {
                'header': _('Shipment on Hold'),
                'field': 'out0',
                'type': 'number',
                'width': 9
            },
            5: {
                'header': _('Shipment'),
                'field': 'out1',
                'type': 'number',
                'width': 9
            },
            6: {
                'header': _('Balance'),
                'field': 'bal2',
                'type': 'number',
                'width': 9
            },
            7: {
                'header': _('Receipt'),
                'field': 'in3',
                'type': 'number',
                'width': 9
            },
            8: {
                'header': _('Shipment'),
                'field': 'out3',
                'type': 'number',
                'width': 9
            },
            9: {
                'header': _('Balance'),
                'field': 'bal3',
                'type': 'number',
                'width': 9
            },
            10: {
                'header': _('Receipt'),
                'field': 'in4',
                'type': 'number',
                'width': 9
            },
            11: {
                'header': _('Shipment'),
                'field': 'out4',
                'type': 'number',
                'width': 9
            },
            12: {
                'header': _('Balance'),
                'field': 'bal4',
                'type': 'number',
                'width': 9
            },
            13: {
                'header': _('Receipt'),
                'field': 'in5',
                'type': 'number',
                'width': 9
            },
            14: {
                'header': _('Shipment'),
                'field': 'out5',
                'type': 'number',
                'width': 9
            },
            15: {
                'header': _('Balance'),
                'field': 'bal5',
                'type': 'number',
                'width': 9
            },
            16: {
                'header': _('Receipt'),
                'field': 'in6',
                'type': 'number',
                'width': 9
            },
            17: {
                'header': _('Shipment'),
                'field': 'out6',
                'type': 'number',
                'width': 9
            },
            18: {
                'header': _('Balance'),
                'field': 'bal6',
                'type': 'number',
                'width': 9
            },
        }

    def _get_report_filters(self, report):
        return [
            [_('Report Date'), report.current_date],
            [_('Threshold Date'), report.threshold_date],
        ]

    def _get_col_count_filter_name(self):
        return 2

    def _get_col_count_filter_value(self):
        return 2

    def _generate_report_content(self, workbook, report):
        title_vals = {
            1: 'Part 1. HK Stock',
            2: 'Part 2. Overseas Stock',
        }
        # for section in report.section_ids:
        #     self.write_array_title(title_vals[section.code])
        #
        #     if section.code == 1:
        #         self.write_array_header()
        #     # adjust array header
        #     elif section.code == 2:
        #         adj_col = {
        #             11: _('Location\n地区'),
        #             12: _('Delivery Days\n预计到港天数'),
        #         }
        #         self.write_array_header(adj_col)
        #
        #     # sort output by category_name and product_name
        #     sorted_lines = sorted(
        #         section.line_ids,
        #         key=lambda x: (x.category_name, x.product_name)
        #     )
        #     for line in sorted_lines:
        #         self.write_line(line, height=50)
        #
        #     # Line break
        #     self.row_pos += 2

        self.write_array_title(title_vals[1])
        self.write_array_header()
        for line in report.line_ids:
            self.write_line(line)

        # Line break
        self.row_pos += 2




        params = [
            {'col': 13, 'vals': ['New Stock!']},
        ]
        self._apply_conditional_format(params)


ShipmentScheduleXlsx(
    'report.stock_shipment_schedule_report.shipment_schedule_report',
    'shipment.schedule.report',
    parser=report_sxw.rml_parse
)
