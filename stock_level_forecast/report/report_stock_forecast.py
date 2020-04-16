# -*- coding: utf-8 -*-
# Copyright 2016-2017 Odoo S.A.
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, tools


class ReportStockForecat(models.Model):
    _inherit = 'report.stock.forecast'

    categ_id = fields.Many2one(
        'product.category',
        string='Product Category',
    )
    sale_ok = fields.Boolean(
        string='Can Be Sold',
    )

    # override the method to add Product Category and Can Be Sold to report
    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_stock_forecast')
        self._cr.execute("""
        CREATE or REPLACE VIEW report_stock_forecast AS (
        SELECT
            MIN(id) as id,
            product_id as product_id,
            date as date,
            sum(product_qty) AS quantity,
            sum(sum(product_qty)) OVER (PARTITION BY product_id ORDER BY date) AS cumulative_quantity,
            categ_id as categ_id,
            sale_ok as sale_ok
        FROM (
            SELECT
                MIN(id) as id,
                MAIN.product_id as product_id,
                SUB.date as date,
                CASE WHEN MAIN.date = SUB.date THEN sum(MAIN.product_qty) ELSE 0 END as product_qty,
                MAIN.categ_id as categ_id,
                MAIN.sale_ok as sale_ok
            FROM (
                SELECT
                    MIN(sq.id) as id,
                    sq.product_id,
                    date_trunc('week', to_date(to_char(CURRENT_DATE, 'YYYY/MM/DD'), 'YYYY/MM/DD')) as date,
                    SUM(sq.qty) AS product_qty,
                    product_template.categ_id as categ_id,
                    product_template.sale_ok as sale_ok
                FROM
                    stock_quant as sq
                    LEFT JOIN product_product ON product_product.id = sq.product_id
                    LEFT JOIN product_template ON product_template.id = product_product.product_tmpl_id
                    LEFT JOIN stock_location location_id ON sq.location_id = location_id.id
                WHERE
                    location_id.usage = 'internal'
                GROUP BY
                    date, sq.product_id, product_template.categ_id, product_template.sale_ok
                UNION ALL
                SELECT
                    MIN(-sm.id) as id,
                    sm.product_id,
                    CASE WHEN sm.date_expected > CURRENT_DATE
                        THEN date_trunc('week', to_date(to_char(sm.date_expected, 'YYYY/MM/DD'), 'YYYY/MM/DD'))
                        ELSE date_trunc('week', to_date(to_char(CURRENT_DATE, 'YYYY/MM/DD'), 'YYYY/MM/DD')) END
                        AS date,
                    SUM(sm.product_qty) AS product_qty,
                    product_template.categ_id as categ_id,
                    product_template.sale_ok as sale_ok
                FROM
                    stock_move as sm
                    LEFT JOIN product_product ON product_product.id = sm.product_id
                    LEFT JOIN product_template ON product_template.id = product_product.product_tmpl_id
                    LEFT JOIN stock_location dest_location ON sm.location_dest_id = dest_location.id
                    LEFT JOIN stock_location source_location ON sm.location_id = source_location.id
                WHERE
                    sm.state IN ('confirmed','assigned','waiting')
                    AND source_location.usage != 'internal'
                    AND dest_location.usage = 'internal'
                GROUP BY
                    sm.date_expected, sm.product_id, product_template.categ_id, product_template.sale_ok
                UNION ALL
                SELECT
                    MIN(-sm.id) AS id,
                    sm.product_id,
                    CASE WHEN sm.date_expected > CURRENT_DATE
                        THEN date_trunc('week', to_date(to_char(sm.date_expected, 'YYYY/MM/DD'), 'YYYY/MM/DD'))
                        ELSE date_trunc('week', to_date(to_char(CURRENT_DATE, 'YYYY/MM/DD'), 'YYYY/MM/DD')) END
                        AS date,
                    SUM(-(sm.product_qty)) AS product_qty,
                    product_template.categ_id as categ_id,
                    product_template.sale_ok as sale_ok
                FROM
                    stock_move AS sm
                    LEFT JOIN product_product ON product_product.id = sm.product_id
                    LEFT JOIN product_template ON product_template.id = product_product.product_tmpl_id
                    LEFT JOIN stock_location source_location ON sm.location_id = source_location.id
                    LEFT JOIN stock_location dest_location ON sm.location_dest_id = dest_location.id
                WHERE
                    sm.state IN ('confirmed','assigned','waiting')
                    AND source_location.usage = 'internal'
                    AND dest_location.usage != 'internal'
                GROUP BY
                    sm.date_expected, sm.product_id, product_template.categ_id, product_template.sale_ok
            ) as MAIN
        LEFT JOIN (
            SELECT DISTINCT date
            FROM (
                SELECT
                    date_trunc('week', CURRENT_DATE) AS DATE
                UNION ALL
                SELECT
                    date_trunc('week', to_date(to_char(sm.date_expected, 'YYYY/MM/DD'), 'YYYY/MM/DD')) AS date
                FROM
                    stock_move sm
                    LEFT JOIN stock_location source_location ON sm.location_id = source_location.id
                    LEFT JOIN stock_location dest_location ON sm.location_dest_id = dest_location.id
                WHERE
                    sm.state IN ('confirmed','assigned','waiting')
                    AND sm.date_expected > CURRENT_DATE
                    AND ((dest_location.usage = 'internal' AND source_location.usage != 'internal')
                        OR (source_location.usage = 'internal' AND dest_location.usage != 'internal'))
                ) AS DATE_SEARCH) SUB ON (SUB.date IS NOT NULL)
        GROUP BY MAIN.product_id, SUB.date, MAIN.date, MAIN.categ_id, MAIN.sale_ok
        ) AS FINAL
        GROUP BY
            product_id, date, categ_id, sale_ok)
        """)
