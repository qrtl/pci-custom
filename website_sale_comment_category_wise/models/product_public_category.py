# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    website_order_comment = fields.Boolean(
        string="Website Order Comment",
        copy=False,
    )
