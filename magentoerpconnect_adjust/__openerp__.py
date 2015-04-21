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

{'name': 'Adjustments to Magento Connector',
 'version': '1.0',
 'category': 'Connector',
 'depends': ['magentoerpconnect',
             ],
 'author': "Rooms For (Hong Kong) Ltd. T/A OSCG",
 'website': 'http://www.openerp-asia.net',
 'description': """
Main Features
=============
- Proposes the correct 'Fiscal Position' for newly imported customers based \
on customer's location (if state is NOT 'CA', fiscal position should be 'Tax \
Exempt'). This should apply to all the customers regardless of dealer/end \
user.
- Sets salesperson of imported sales order based on the customer master \
setting of the customer of the sales order. In case there is no salesperson \
found in the customer master, propose a default salesperson in sales order.
""",
 'images': [],
 'demo': [],
 'data': [
          'view/res_users_view.xml',
          'view/partner_view.xml',
          ],
 'installable': True,
 'application': True,
 }
