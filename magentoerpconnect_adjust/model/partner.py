# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved
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
#

from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_fiscal_position(osv.osv):
    _inherit = 'account.fiscal.position'
    _columns = {
        'magento_taxexempt': fields.boolean('Magento Tax Exempt',
            help='Indicates the fiscal position to be set for "tax exempt" \
            partners imported from Magento.'),
    }

    def _check_magento_taxexempt(self, cr, uid, ids, context=None):
        record_exists = False
        fp_ids = self.search(cr, uid, [])
        for record in self.browse(cr, uid, fp_ids, context=context):
            if record_exists and record.magento_taxexempt:
                return False
            elif record.magento_taxexempt:
                record_exists = True
        return True

    _constraints = [
        (_check_magento_taxexempt, 'You cannot select more than one \
            fiscal position to be the "tax exempt" fiscal position for \
            Magento.', ['magento_taxexempt']),
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
