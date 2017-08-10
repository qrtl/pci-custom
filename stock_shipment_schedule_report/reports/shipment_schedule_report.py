# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, fields, _
from openerp.addons.abstract_report_xlsx.reports \
    import stock_abstract_report_xlsx
from openerp.report import report_sxw


class ScheduleReport(models.TransientModel):
    """ Here, we just define class fields.
    For methods, go more bottom at this file.

    The class hierarchy is :
    * ConsignmentReport
    ** ConsignmentReportSection
    *** ConsignmentReportQuant
    """

    _name = 'schedule.report'

    new_stock_days = fields.Integer()
    stock_threshold_date = fields.Date()
    current_date = fields.Date(
        default=fields.Date.context_today
    )
    cny_rate = fields.Float()

    # # Data fields, used to browse report data
    # section_ids = fields.One2many(
    #     comodel_name='offer.report.section',
    #     inverse_name='report_id'
    # )
    # line_ids = fields.One2many(
    #     comodel_name='offer.report.line',
    #     inverse_name='report_id'
    # )


# class OfferReportSection(models.TransientModel):
#
#     _name = 'offer.report.section'
#
#     report_id = fields.Many2one(
#         comodel_name='offer.report',
#         ondelete='cascade',
#         index=True
#     )
#     line_ids = fields.One2many(
#         comodel_name='offer.report.line',
#         inverse_name='section_id'
#     )
#
#     # Data fields, used for report display
#     code = fields.Integer()
#
#
class ScheduleReportLine(models.TransientModel):
    _name = 'schedule.report.line'
#
#     report_id = fields.Many2one(
#         comodel_name='offer.report',
#         ondelete='cascade',
#         index=True
#     )
#     section_id = fields.Many2one(
#         comodel_name='offer.report.section',
#         ondelete='cascade',
#         index=True
#     )
#
#     # Data fields, used to keep link with real object
#     product_id = fields.Many2one(
#         'product.product',
#         index=True
#     )
#     quant_id = fields.Many2one(
#         'stock.quant',
#     )
#     supp_stock_id = fields.Many2one(
#         'supplier.stock',
#     )
#     owner_id = fields.Many2one(
#         'res.partner',
#         index=True
#     )
#
#     # Data fields, used for report display
#     category_name = fields.Char()
#     product_code = fields.Char()
#     product_name = fields.Char()
#     qty = fields.Integer()
#     image_small = fields.Binary()
#     list_price = fields.Float()
#     owner_name = fields.Char()
#     unit_cost = fields.Float(digits=(16, 2))
#     cost_discount = fields.Float()
#     status = fields.Char()
#     net_price = fields.Float()
#     net_price_cny = fields.Float()
#     net_profit = fields.Float()  # net_price - unit_cost
#     profit_percent = fields.Float()
#     sale_discount = fields.Float()
#     remark = fields.Char()  # to show status
#     placeholder1 = fields.Char()
#     outgoing_date = fields.Datetime()
#     move_date = fields.Datetime()  # for report presentation
#     stock_days = fields.Integer()
#
#
class ShipmentScheduleReportCompute(models.TransientModel):
    # only methods are defined here
    _inherit = 'schedule.report'

    @api.multi
    def print_report(self):
        self.ensure_one()
        self.compute_data_for_report()
        report_name = 'stock_shipment_schedule_report.schedule_report'
        return self.env['report'].get_action(self, report_name)

    def _prepare_report_xlsx(self):
        self.ensure_one()
        return {
            'threshold_date': self.threshold_date,
            'categ_id': self.categ_id,
        }

    @api.multi
    def compute_data_for_report(self):
        self.ensure_one()
        model = self.env['schedule.report.line']
        # self._create_section_records()
        # sections = self.env['offer.report.section'].search(
        #     [('report_id', '=', self.id)])
        # for section in sections:
        #     self._inject_quant_values(section)
        #     if section.code == 2:
        #         self._update_overseas_stock_fields(model, section)
        #     self._update_qty(model, section)
        #     self._update_owner(model, section)
        #     if section.code == 1:
        #         self._update_age(model, section)
        #     self._update_remark(model, section)
        self.refresh()
#
#     def _create_section_records(self):
#         model = self.env['offer.report.section']
#         for i in [1, 2]:
#             vals = {
#                 'report_id': self.id,
#                 'code': i
#             }
#             model.create(vals)
#
#     def _inject_quant_values(self, section):
#         if section.code == 1:
#             query = """
#             INSERT INTO
#                 offer_report_line
#                 (
#                 report_id,
#                 section_id,
#                 create_uid,
#                 create_date,
#                 category_name,
#                 quant_id,
#                 owner_id,
#                 product_id,
#                 product_code,
#                 product_name,
#                 image_small,
#                 list_price,
#                 unit_cost,
#                 net_price,
#                 placeholder1
#                 )
#             SELECT DISTINCT ON (p.name_template)
#                 %s AS report_id,
#                 %s AS section_id,
#                 %s AS create_uid,
#                 NOW() AS create_date,
#                 pc.name,
#                 q.id,
#                 q.original_owner_id,
#                 p.id,
#                 p.default_code,
#                 p.name_template,
#                 pt.image_small,
#                 pt.list_price,
#                 q.cost,
#                 pt.net_price,
#                 q.in_date
#             FROM
#                 stock_quant q
#             INNER JOIN
#                 product_product p ON q.product_id = p.id
#             INNER JOIN
#                 product_template pt ON p.product_tmpl_id = pt.id
#             INNER JOIN
#                 product_category pc ON pt.categ_id = pc.id
#             INNER JOIN
#                 stock_location loc ON q.location_id = loc.id
#             WHERE
#                 loc.usage = 'internal'
#                 AND q.reservation_id is null
#                 AND q.sale_id is null
#                 AND q.in_date >= %s
#             """
#             query_params = (
#                 self.id,
#                 section.id,
#                 self.env.uid,
#                 section.report_id.stock_threshold_date or '1900-01-01',
#             )
#         if section.code == 2:
#             query = """
#             INSERT INTO
#                 offer_report_line
#                 (
#                 report_id,
#                 section_id,
#                 create_uid,
#                 create_date,
#                 category_name,
#                 supp_stock_id,
#                 owner_id,
#                 product_id,
#                 product_code,
#                 product_name,
#                 image_small,
#                 list_price,
#                 net_price
#                 )
#             SELECT DISTINCT ON (p.name_template)
#                 %s AS report_id,
#                 %s AS section_id,
#                 %s AS create_uid,
#                 NOW() AS create_date,
#                 pc.name,
#                 ss.id,
#                 ss.partner_id,
#                 p.id,
#                 p.default_code,
#                 p.name_template,
#                 pt.image_small,
#                 pt.list_price,
#                 pt.net_price
#             FROM
#                 supplier_stock ss
#             INNER JOIN
#                 product_product p ON ss.product_id = p.id
#             INNER JOIN
#                 product_template pt ON p.product_tmpl_id = pt.id
#             INNER JOIN
#                 product_category pc ON pt.categ_id = pc.id
#             """
#             query_params = (
#                 self.id,
#                 section.id,
#                 self.env.uid,
#             )
#         self.env.cr.execute(query, query_params)
#
#     # this method is for sction code 2
#     def _update_overseas_stock_fields(self, model, section):
#         lines = model.search([('section_id', '=', section.id)])
#         ss_obj = self.env['supplier.stock']
#         for line in lines:
#             lowest_cost = 0.0
#             ss_recs = ss_obj.search([('product_id', '=', line.product_id.id)])
#             for r in ss_recs:
#                 if not lowest_cost or r.price_unit_base < lowest_cost:
#                     lowest_cost = r.price_unit_base
#                     r_id = r.id
#             rec = ss_obj.browse(r_id)
#             line.write({
#                 'unit_cost': rec.price_unit_base,
#                 'placeholder1': rec.partner_loc_id.name,
#                 'owner_id': rec.partner_id.id,
#                 'stock_days': rec.supplier_lead_time,
#             })
#
#     def _update_qty(self, model, section):
#         locs = self.env['stock.location'].search([
#             ('usage', '=', 'internal'),
#             ('active', '=', True),
#             ('is_repair_location', '=', False),
#         ])
#         lines = model.search([('section_id', '=', section.id)])
#         for line in lines:
#             qty = 1
#             if section.code == 1:
#                 qty = self.env['stock.quant'].search_count([
#                     ('product_id', '=', line.product_id.id),
#                     ('location_id', 'in', [loc.id for loc in locs]),
#                 ])
#             elif section.code == 2:
#                 qty = self.env['supplier.stock'].search_count([
#                     ('product_id', '=', line.product_id.id),
#                 ])
#             if line.list_price:
#                 cost_discount = 1 - (line.unit_cost / line.list_price)
#                 sale_discount = 1 - (line.net_price / line.list_price)
#             else:
#                 cost_discount = 0.0
#                 sale_discount = 0.0
#             net_profit = line.net_price - line.unit_cost
#             if line.unit_cost:
#                 profit_percent = net_profit / line.unit_cost
#             else:
#                 profit_percent = 9.9999
#             net_price_cny = line.net_price * line.report_id.cny_rate
#             line.write({
#                 'qty': qty,
#                 'cost_discount': cost_discount,
#                 'sale_discount': sale_discount,
#                 'net_profit': net_profit,
#                 'profit_percent': profit_percent,
#                 'net_price_cny': net_price_cny,
#             })
#
#     def _update_owner(self, model, section):
#         lines = model.search([('section_id', '=', section.id)])
#         for line in lines:
#             if line.owner_id.ref:
#                 owner_name = line.owner_id.ref
#             else:
#                 owner_name = line.owner_id.name
#             line.owner_name = owner_name
#
#     # this method is for section code 1
#     def _update_age(self, model, section):
#         lines = model.search([('section_id', '=', section.id)])
#         for line in lines:
#             out_date = fields.Datetime.now()
#             if section.code == 1:
#                 move_date = line.placeholder1
#                 stock_days = (
#                     fields.Datetime.from_string(out_date) - \
#                     fields.Datetime.from_string(line.placeholder1)
#                 ).days
#                 line.write({
#                     'outgoing_date': out_date,
#                     'move_date': move_date,
#                     'stock_days': stock_days,
#                 })
#
#     def _update_remark(self, model, section):
#         lines = model.search([('section_id', '=', section.id)])
#         for line in lines:
#             if section.code == 1:
#                 if line.stock_days <= self.new_stock_days:
#                     status = 'New Stock!'
#                 else:
#                     status = 'In Stock'
#             if section.code == 2:
#                 status = 'Overseas Stock'
#             line.remark = status
#
#
# class StockOfferXslx(stock_abstract_report_xlsx.StockAbstractReportXslx):
#
#     def __init__(self, name, table, rml=False, parser=False, header=True,
#                  store=False):
#         super(StockOfferXslx, self).__init__(
#             name, table, rml, parser, header, store)
#
#     def _get_report_name(self):
#         return _('Stock Offer Report')
#
#     def _get_report_columns(self, report):
#         return {
#             0: {'header': _('Brand\n品牌'), 'field': 'category_name',
#                 'width': 20},
#             1: {'header': _('Image\n图片'), 'field': 'image_small',
#                 'type': 'image', 'width': 10},
#             2: {'header': _('Code\n代码'), 'field': 'product_code',
#                 'width': 10},
#             3: {'header': _('Reference Name\n型号'), 'field': 'product_name',
#                 'width': 30},
#             4: {'header': _('Qty\n数量'), 'field': 'qty', 'type': 'number',
#                 'width': 5},
#             5: {'header': _('HK Retail\n港币公价'), 'field': 'list_price',
#                 'type': 'amount', 'width': 12},
#             6: {'header': _('Owner/Contact Ref.\n货主'), 'field': 'owner_name',
#                  'width': 18},
#             7: {'header': _('Unit Cost\n港币来价'), 'field': 'unit_cost',
#                 'type': 'amount', 'width': 12},
#             8: {'header': _('Cost Discount\n港币来价%'),
#                 'field': 'cost_discount', 'type': 'percent', 'width': 9},
#             9: {'header': _('Net Profit\n利润'), 'field': 'net_profit',
#                 'type': 'amount', 'width': 12},
#             10: {'header': _('Profit %\n利润%'), 'field': 'profit_percent',
#                 'type': 'percent', 'width': 9},
#             11: {'header': _('Incoming Date\n入库时间'),
#                  'field': 'placeholder1', 'width': 18},
#             12: {'header': _('Days in Stock\n库存天数'), 'field': 'stock_days',
#                  'type': 'number', 'width': 10},
#             13: {'header': _('Status\n库存状态'), 'field': 'remark',
#                  'width': 15},
#             14: {'header': _('Sales Discount\n港币扣点'),
#                  'field': 'sale_discount', 'type': 'percent', 'width': 9},
#             15: {'header': _('Sales Price\n港币卖价'), 'field': 'net_price',
#                  'type': 'amount', 'width': 12},
#             16: {'header': _('Sales Price (CNY)\n当日人民币卖价'),
#                  'field': 'net_price_cny', 'type': 'amount', 'width': 12},
#         }
#
#     def _get_report_filters(self, report):
#         return [
#             [_('Report Date'), report.current_date],
#             [_('New Stock Days'), report.new_stock_days],
#             [_('Stock Threshold Date'), report.stock_threshold_date],
#             [_('CNY Rate'), report.cny_rate],
#         ]
#
#     def _get_col_count_filter_name(self):
#         return 2
#
#     def _get_col_count_filter_value(self):
#         return 2
#
#     def _generate_report_content(self, workbook, report):
#         title_vals = {
#             1: 'Part 1. HK Stock',
#             2: 'Part 2. Overseas Stock',
#         }
#         for section in report.section_ids:
#             self.write_array_title(title_vals[section.code])
#
#             if section.code == 1:
#                 self.write_array_header()
#             # adjust array header
#             elif section.code == 2:
#                 adj_col = {
#                     11: _('Location\n地区'),
#                     12: _('Delivery Days\n预计到港天数'),
#                 }
#                 self.write_array_header(adj_col)
#
#             # sort output by category_name and product_name
#             sorted_lines = sorted(
#                 section.line_ids,
#                 key=lambda x: (x.category_name, x.product_name)
#             )
#             for line in sorted_lines:
#                 self.write_line(line, height=50)
#
#             # Line break
#             self.row_pos += 2
#
#         params = [
#             {'col': 13, 'vals': ['New Stock!']},
#         ]
#         self._apply_conditional_format(params)
#
#
# StockOfferXslx(
#     'report.stock_offer_report.offer_report',
#     'offer.report',
#     parser=report_sxw.rml_parse
# )
