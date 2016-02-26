# -*- coding: utf-8 -*-
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG
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

import logging
from openerp.tools.translate import _
from openerp.addons.connector.unit.mapper import mapping
from openerp.addons.magentoerpconnect.backend import magento
from openerp.addons.magentoerpconnect.sale import (SaleOrderImportMapper,
                                                   SaleOrderBatchImport)

from openerp import SUPERUSER_ID
import pytz
from datetime import datetime

_logger = logging.getLogger(__name__)


@magento(replacing=SaleOrderBatchImport)
class MySaleOrderBatchImport(SaleOrderBatchImport):
    _model_name = ['magento.sale.order']

    def run(self, filters=None):
        """ Run the synchronization """
        if filters is None:
            filters = {}
#         filters['state'] = {'neq': 'canceled'}  # changed by oscg
        filters['state'] = {'nin': ['canceled', 'pending_payment']}  # changed by oscg
        from_date = filters.pop('from_date', None)
        to_date = filters.pop('to_date', None)
        magento_storeview_ids = [filters.pop('magento_storeview_id')]
        record_ids = self.backend_adapter.search(
            filters,
            from_date=from_date,
            to_date=to_date,
            magento_storeview_ids=magento_storeview_ids)
        _logger.info('search for magento saleorders %s returned %s',
                     filters, record_ids)
        for record_id in record_ids:
            self._import_record(record_id)


@magento(replacing=SaleOrderImportMapper)
class MySaleOrderImportMapper(SaleOrderImportMapper):
    _model_name = 'magento.sale.order'
 
    @mapping
    def date_order(self, record):
        # adjust the order date according to superuser's time zone
        # ('created_at' in magento is kept in UTC)
        session = self.session
        user = session.browse('res.users', SUPERUSER_ID)
        if user.partner_id.tz:
            tz = pytz.timezone(user.partner_id.tz)
        else:
            tz = pytz.utc
        created_at_tz = pytz.utc.localize(datetime.strptime(record['created_at'], '%Y-%m-%d %H:%M:%S')).astimezone(tz).strftime('%Y-%m-%d')
        return {'date_order': created_at_tz}
    
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
