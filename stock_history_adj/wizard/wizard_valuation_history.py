# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _


class WizardValuationHistory(models.TransientModel):
    _inherit = 'wizard.valuation.history'

    @api.multi
    def open_table(self):
        """
        add search_default_filter_stockable_products in context
        """
        self.ensure_one()
        ctx = dict(
            self._context,
            history_date=self.date,
            search_default_filter_stockable_products=True,
            search_default_group_by_product=True,
            search_default_group_by_location=True)

        action = self.env['ir.model.data'].xmlid_to_object('stock_account.action_stock_history')
        if not action:
            action = {
                'view_type': 'form',
                'view_mode': 'tree,graph,pivot',
                'res_model': 'stock.history',
                'type': 'ir.actions.act_window',
            }
        else:
            action = action[0].read()[0]

        action['domain'] = "[('date', '<=', '" + self.date + "')]"
        action['name'] = _('Stock Value At Date')
        action['context'] = ctx
        return action
