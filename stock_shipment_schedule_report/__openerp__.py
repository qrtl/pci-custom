# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved.
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
##############################################################################

{
    'name': 'Shipment Schedule Report',
    'version': '1.0',
    'category': "Report",
    'summary': 'Adds a report function to print stock projection',
    'description': """
* Adds a menu item 'Shipment Schedule Report'.
* Shows shipment quantities for future periods for each product (with incoming quantities and projected QOH as well).
* Shipment and receipt quantities are taken from stock moves; only confirmed orders are considered.
* This function does not filter output by warehouse/location. 
     """,
    'author': 'Rooms For (Hong Kong) T/A OSCG',
    'depends': ['sale_stock','report_aeroo_ooo','report_aeroo'],
    'init_xml': [],
    'update_xml': [
        'wizard/shipment_schedule_wizard.xml',
        'shipment_schedule.xml',
    ],

    'demo_xml': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
