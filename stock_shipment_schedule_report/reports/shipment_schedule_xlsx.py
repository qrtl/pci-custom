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
            0: {'header': _('Product'), 'field': 'product_name',
                'width': 20},
            1: {'header': _('Product Category'), 'field': 'categ_name',
                'width': 10},
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
