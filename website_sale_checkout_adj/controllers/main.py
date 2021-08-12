# -*- coding: utf-8 -*-

from odoo.addons.website_sale.controllers.main import WebsiteSale

class RequireZipCode(WebsiteSale):

    def _get_mandatory_billing_fields(self):
      res = super(RequireZipCode, self)._get_mandatory_billing_fields()
      return res + ["zip"]

    def _get_mandatory_shipping_fields(self):
      res = super(RequireZipCode, self)._get_mandatory_shipping_fields()
      return res + ["zip"]
