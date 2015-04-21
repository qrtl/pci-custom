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

from openerp.tools.translate import _
from openerp.addons.connector.unit.mapper import mapping
from openerp.addons.magentoerpconnect.backend import magento
from openerp.addons.magentoerpconnect.sale import SaleOrderImportMapper


@magento(replacing=SaleOrderImportMapper)
class MySaleOrderImportMapper(SaleOrderImportMapper):
    _model_name = 'magento.sale.order'
 
    @mapping
    def user_id(self, record):
        """ Assign the salesperson of the partner if any """
        session = self.session
        partner_rec = session.browse('res.partner', self.options.partner_id)
        if partner_rec.user_id:
            return {'user_id': partner_rec.user_id.id}
        user_ids = session.search('res.users',
            [('magento_salesperson_default','=',True)])
        if user_ids:
            return {'user_id': user_ids[0]}
        return {'user_id': False}
