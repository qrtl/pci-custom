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

from openerp.addons.connector.unit.mapper import mapping
from openerp.addons.magentoerpconnect.backend import magento
from openerp.addons.magentoerpconnect.partner import AddressImportMapper


@magento(replacing=AddressImportMapper)
class MyAddressImportMapper(AddressImportMapper):

    @mapping
    def property_account_position(self, record):
        if not record.get('region'):
            return
        session = self.session
        state_ids = session.search('res.country.state',
            [('name', '=ilike', record['region'])])
        if state_ids and session.browse('res.country.state',
            state_ids)[0].code == 'CA':
            return
        fp_ids = session.search('account.fiscal.position',
            [('magento_taxexempt','=',True)])
        if fp_ids:
            return {'property_account_position': fp_ids[0]}
        return
