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


class res_users(osv.osv):
    _inherit = 'res.users'

    _columns = {
        'magento_salesperson_default': fields.boolean('Default Magento \
            Salesperson', help="Indicates the default salesperson to be set \
            in sales orders imported from Magento, in case salesperson is \
            not set in customer master."),
    }

    def _check_magento_salesperson_default(self, cr, uid, ids, context=None):
        default_exists = False
        user_ids = self.search(cr, uid, [])
        for record in self.browse(cr, uid, user_ids, context=context):
            if default_exists and record.magento_salesperson_default:
                return False
            elif record.magento_salesperson_default:
                default_exists = True
        return True

    _constraints = [
        (_check_magento_salesperson_default, 'You cannot select more than one \
            user to be the default salesperson for Magento sales orders.',
            ['magento_salesperson_default']),
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
