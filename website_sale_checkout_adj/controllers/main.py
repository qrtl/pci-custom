# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.addons.website_sale.controllers.main import WebsiteSale


class RequireZipCode(WebsiteSale):
    def _get_mandatory_billing_fields(self):
        res = super(RequireZipCode, self)._get_mandatory_billing_fields()
        return res + ["zip"]

    def _get_mandatory_shipping_fields(self):
        res = super(RequireZipCode, self)._get_mandatory_shipping_fields()
        return res + ["zip"]
