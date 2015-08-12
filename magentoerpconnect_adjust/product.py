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

from openerp.addons.connector.unit.mapper import mapping
from openerp.addons.magentoerpconnect.backend import magento
from openerp.addons.magentoerpconnect.product import ProductImportMapper


@magento(replacing=ProductImportMapper)
class MyProductImportMapper(ProductImportMapper):

    @mapping
    def description_sale(self, record):
        """ Override the mapping to make this field blank so that the
        description with HTML tags (which comes from Magento) should not
        mess up the product description in OpenERP orders """
        return {'description_sale': False}
