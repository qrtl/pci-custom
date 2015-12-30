# -*- coding: utf-8 -*-
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Rooms For (Hong Kong) Limited T/A OSCG
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

{
    "name": "Account Batch Invoice Payment",
    "author": "Rooms For (Hong Kong) Limited T/A OSCG",
    "version": "0.5",
    "category": "Accounting",
    'website': 'www.odoo-asia.com',
    "depends": ["account",
                "shipment_day",
                "connector_ecommerce"],
     'description':'''
- Adds a wizard to batch process validation and payment for certain invoices.
- Adds a scheduled action to batch process validation and payment for certain invoices.
''',
    "data": ['sale_view.xml',
             'data/account_batch_invoice_payment_cron.xml',
             'wizard/account_batch_invoice_payment_view.xml'],
    "installable": True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
