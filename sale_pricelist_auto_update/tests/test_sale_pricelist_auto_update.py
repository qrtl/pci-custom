# -*- coding: utf-8 -*-
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestSalePricelistAutoUpdate(SavepointCase):
    post_install = True
    at_install = False

    @classmethod
    def setUpClass(cls):
        super(TestSalePricelistAutoUpdate, cls).setUpClass()
        cls.yearly_sales = cls.env["partner.yearly_sales"]
        range_type = cls.env["date.range.type"].create(
            {"name": "Fiscal Year", "is_fiscal_year": True,}
        )
        cls.date_range = cls.env["date.range"].create(
            {
                "name": "FY2022",
                "date_start": "2022-01-01",
                "date_end": "2022-12-31",
                "type_id": range_type.id,
            }
        )
        acc_receivable = cls.env["account.account"].create(
            {
                "code": "X4040",
                "name": "Debtors Test",
                "user_type_id": cls.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "property_account_receivable_id": acc_receivable.id,
            }
        )
        product1 = cls.env["product.product"].create(
            {"name": "test product", "type": "consu", "invoice_policy": "delivery",}
        )
        cls.order = cls.env["sale.order"].create({"partner_id": cls.partner.id,})
        cls.env["sale.order.line"].create(
            {"order_id": cls.order.id, "product_id": product1.id, "price_unit": 10.0,}
        )

    def test_confirm_and_cancel_sales_order(self):
        yearly_sales_dom = [
            ("partner_id", "=", self.partner.id),
            ("start_date", "=", "2022-01-01"),
            ("end_date", "=", "2022-12-31"),
        ]
        yearly_sales = self.yearly_sales.search(yearly_sales_dom)
        # No corresponding yearly sales record before sales order confirmation.
        self.assertEqual(yearly_sales.id, False)

        self.order.action_confirm()
        self.order.write({"date_order_ctx": "2022-01-20"})
        yearly_sales = self.yearly_sales.search(yearly_sales_dom)
        self.assertEqual(yearly_sales.amt_computed, 10.0)

        self.order.action_cancel()
        self.assertEqual(yearly_sales.amt_computed, 0.0)
