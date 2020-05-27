# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request


class WebsiteSale(http.Controller):

    @http.route(['/shop/order/note'], type='json', auth="public", website=True)
    def order_note(self, note, **post):
        order = request.website.sudo().sale_get_order()
        if order:
            order.sudo().note = note
