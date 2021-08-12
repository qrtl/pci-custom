# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale

class RequireZipCode(WebsiteSale):
    @http.route(['/shop/address',], type='http', auth="public", website=True)

    def _get_mandatory_billing_fields(self):
      res = super(RequireZipCode, self)._get_mandatory_billing_fields()
      return res + ["zip"]

    def _get_mandatory_shipping_fields(self):
      res = super(RequireZipCode, self)._get_mandatory_shipping_fields()
      return res + ["zip"]
