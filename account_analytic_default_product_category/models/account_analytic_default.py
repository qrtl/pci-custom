# -*- coding: utf-8 -*-
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016 Rooms For (Hong Kong) Limited T/A OSCG
#    <https://www.odoo-asia.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp.osv import osv

class account_analytic_default(osv.osv):
    _inherit = "account.analytic.default"

    def account_get(self, cr, uid, product_id=None, partner_id=None, user_id=None, date=None, context=None):
        categ = self.pool.get('product.product').browse(cr, uid, product_id, context=context).categ_id
        if categ.analytic_id:
            return categ
        else:
            res = super(account_analytic_default, self).account_get(cr, uid, product_id, partner_id, user_id, date, context=context)
            return res

account_analytic_default()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
