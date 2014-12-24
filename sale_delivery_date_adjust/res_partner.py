# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Rooms For (Hong Kong) Limited T/A OSCG
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

from openerp.osv import fields, osv


class res_partner_category(osv.osv):
    _inherit = 'res.partner.category'
    _columns = {
        'scheduled_time': fields.boolean('Scheduled Time Proposal'),
        'cutoff': fields.boolean('Apply Cutoff Day'),
        #'cutoff_day': fields.integer('Cutoff Day'),
        'cutoff_day': fields.selection([('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday'),], 'Cutoff Day'),
        'days_added': fields.integer('Days to Add'),
    }

res_partner_category() 

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
