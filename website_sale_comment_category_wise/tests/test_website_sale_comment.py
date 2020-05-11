# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from odoo.addons.website_sale_comment_category_wise.controllers.main import WebsiteSale
import odoo.tests
from odoo import http
from mock import patch
from odoo.addons.website_sale_comment_category_wise.controllers.main \
    import WebsiteSale
from odoo.api import Environment


@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class TestWebsiteSaleComment(odoo.tests.HttpCase):
    def setUp(self):
        super(TestWebsiteSaleComment, self).setUp()
        self.website = self.env["website"].browse(1)
        self.WebsiteSaleController = WebsiteSale()

        # with self.phantom_js("/shop/order/note", "odoo.__DEBUG__.services['web_tour.tour'].run('order_note')",
        #                      "odoo.__DEBUG__.services['web_tour.tour'].tours.order_note.ready", login='admin'):
        #     note = "test-comment"
        #     for order in env['sale.order'].search([]):
        #     # controller.order_note(note=note, **{})
        #         self.assertEqual(order.note, note, "Test-Comment Added to SaleOrder")

    # TEST WEBSITE SALE COMMENT
    def test_01_create_website_sale_comment(self):
        partner = self.env.user.partner_id
        so = self._create_so(partner.id)
        print("fffffffffffffffffffffffffffffffffffffffffff",so)
        # with patch.object(http, '/shop/order/note') as request:
        #     request.env = self.env
        # controller = WebsiteSale()
        note = "test-comment"
        # controller.order_note(note=note, **{})
        #
        # with self.phantom_js("/shop/order/note", "", "", login='admin'):
        cr = self.registry.cursor()
        assert cr == self.registry.test_cr
        env = Environment(cr, self.uid, {})

        with patch(env, website=self.website, sale_order_id=so.id):
            self.WebsiteSaleController.order_note(note=note, **{})
            self.assertEqual(so.note, note, "Test-Comment Added to SaleOrder")

    def _create_so(self, partner_id=None):
        print("xxxxxxxxxxxxxxxxxxxxxxxxx")
        print("xxxxxxxxxxxxxxxxxxxxxxxxx")
        print("xxxxxxxxxxxxxxxxxxxxxxxxx")
        print("xxxxxxxxxxxxxxxxxxxxxxxxx")
        print("xxxxxxxxxxxxxxxxxxxxxxxxx")
        print("xxxxxxxxxxxxxxxxxxxxxxxxx")
        return self.env["sale.order"].create(
            {
                "partner_id": partner_id,
                "website_id": self.website.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.env["product.product"]
                            .create({"name": "Product A", "list_price": 100})
                            .id,
                            "name": "Product A",
                        },
                    )
                ],
            }
        )
