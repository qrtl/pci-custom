# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import urlparse

from odoo.addons.payment_paypal.controllers.main import PaypalController
from odoo.http import request
from odoo import models, fields, api


class AcquirerPaypal(models.Model):
    _inherit = 'payment.acquirer'

    @api.multi
    def paypal_form_generate_values(self, values):
        paypal_tx_values = super(AcquirerPaypal,
                                 self).paypal_form_generate_values(values)
        base_url = "https://" + request.httprequest.environ.get('HTTP_HOST', '')
        paypal_tx_values.update({
            'paypal_return': '%s' % urlparse.urljoin(base_url,
                                                     PaypalController._return_url),
            'notify_url': '%s' % urlparse.urljoin(base_url,
                                                  PaypalController._notify_url),
            'cancel_return': '%s' % urlparse.urljoin(base_url,
                                                     PaypalController._cancel_url),
        })
        return paypal_tx_values
