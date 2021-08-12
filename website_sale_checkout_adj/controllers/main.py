# -*- coding: utf-8 -*-

from odoo.addons.website_sale.controllers.main import WebsiteSale

class RequireZipCode(WebsiteSale):
    def _get_mandatory_billing_fields(self):
      return ["name", "email", "street", "city", "zip", "country_id"]

    def _get_mandatory_shipping_fields(self):
        return ["name", "street", "city", "zip", "country_id"]
