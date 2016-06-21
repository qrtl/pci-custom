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
    
    'name' : 'Auto MO Produce',
    'version' : '1.0',
    'depends' : ['mrp'],
    'author' : 'Rooms For (Hong Kong) Limited T/A OSCG',
    'website' : 'http://odoo-asia.com',
    'description': '''
This module runs scheduler every day for produce mo which are ready to produce.
                ''',
    'category' : 'Manufacturing',
    'sequence': 70,
    'data' : [
        'views/auto_mo_produce_data.xml',
        'views/auto_mo_produce.xml',
        'security/ir.model.access.csv'
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
