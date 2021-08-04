# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountAnalyticDefault(models.Model):
    _inherit = "account.analytic.default"

    @api.model
    def account_get(
        self, product_id=None, partner_id=None, user_id=None, date=None, company_id=None
    ):
        res = super(AccountAnalyticDefault, self).account_get(
            product_id, partner_id, user_id, date, company_id
        )
        if not res:
            categ = self.env["product.product"].browse(product_id).categ_id
            if categ.analytic_id:
                res = categ
        return res
