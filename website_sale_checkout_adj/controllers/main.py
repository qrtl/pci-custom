from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class RequireZipCode(WebsiteSale):
    
    def _get_mandatory_shipping_fields(self):
        return ["name", "street", "city", "country_id", "zip"]
        