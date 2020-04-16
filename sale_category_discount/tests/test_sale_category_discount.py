# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class SaleCategoryDiscount(common.TransactionCase):
    post_install = True

    def setUp(self):
        super(SaleCategoryDiscount, self).setUp()
        # Test portal user record
        self.partner = self.env.ref('portal.demo_user0').partner_id
        self.test_product = self.env.ref(
            'product.product_product_7_product_template')
        # Test delivery method
        self.delivery_method = self.env['delivery.carrier'].create(dict(
            name='Test Delivery',
            delivery_type='base_on_rule',
        ))
        self.delivery_rule_1 = self.env['delivery.price.rule'].create(dict(
            carrier_id=self.delivery_method.id,
            variable='price',
            operator='>=',
            max_value=80,
            list_base_price=0,
            standard_price=0,
        ))
        self.delivery_rule_2 = self.env['delivery.price.rule'].create(dict(
            carrier_id=self.delivery_method.id,
            variable='price',
            operator='<',
            max_value=80,
            list_base_price=10,
            standard_price=10,
        ))

    def test_00_quotation_with_delivery(self):
        quotation = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'pricelist_id': self.partner.property_product_pricelist.id,
            'carrier_id': self.delivery_method.id,
        })
        self.env['sale.order.line'].create({
            'name': self.test_product.name,
            'order_id': quotation.id,
            'product_id': self.test_product.id,
            'price_unit': 79,
            'product_uom_qty': 1,
            'fixed_price': True,
        })
        quotation.delivery_set()
        delivery_order_line = quotation.order_line.filtered(
            lambda x: x.is_delivery)
        self.assertEqual(delivery_order_line.price_unit, 10)

    def test_01_quotation_free_delivery(self):
        quotation = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'pricelist_id': self.partner.property_product_pricelist.id,
            'carrier_id': self.delivery_method.id,
        })
        self.env['sale.order.line'].create({
            'name': self.test_product.name,
            'order_id': quotation.id,
            'product_id': self.test_product.id,
            'price_unit': 79,
            'product_uom_qty': 2,
            'fixed_price': True,
        })
        quotation.delivery_set()
        delivery_order_line = quotation.order_line.filtered(
            lambda x: x.is_delivery)
        self.assertEqual(delivery_order_line.price_unit, 0)
