# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, fields, _
# from openerp.addons.abstract_report_xlsx.reports \
#     import stock_abstract_report_xlsx
# from openerp.report import report_sxw


class ScheduleReport(models.TransientModel):
    # class fields are defined here
    _name = 'schedule.report'

    threshold_date = fields.Date()
    current_date = fields.Date(
        default=fields.Date.context_today
    )

    # # Data fields, used to browse report data
    line_ids = fields.One2many(
        comodel_name='schedule.report.line',
        inverse_name='report_id'
    )


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

    report_id = fields.Many2one(
        comodel_name='schedule.report',
        ondelete='cascade',
        index=True,
    )
    product_name = fields.Char()
    categ_name = fields.Char()


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
        self._inject_quant_values()

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
    def _inject_quant_values(self):
        query = """
        INSERT INTO
            schedule_report_line
            (
            report_id,
            create_uid,
            create_date,
            product_name,
            categ_name
            )
        SELECT
            %s AS report_id,
            %s AS create_uid,
            NOW() AS create_date,
            pt.name,
            pc.name
        FROM
            product_product pp
        INNER JOIN
            product_template pt ON pp.product_tmpl_id = pt.id
        INNER JOIN
            product_category pc ON pt.categ_id = pc.id
        """
        query_params = (
            self.id,
            self.env.uid,
        )
        self.env.cr.execute(query, query_params)



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
