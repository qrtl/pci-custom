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

from osv import osv, fields
import netsvc
from tools.translate import _
import openerp.addons.decimal_precision as dp
import time


class account_period(osv.osv):
    _inherit = "account.period"
    
    _columns = {
        
    }
    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args=[]
        if not context:
            context={}
        ids = []
        period_ids = []
        sql = ''
        if context.get('con_period_unit', False) and context['con_period_unit'] =='qtr':
            if context.get('con_fiscalyear_id', False):
                sql = """
                    select id from account_period
                    where fiscalyear_id = %s
                    and (code ilike '%s' or code ilike '%s' or code ilike '%s' or code ilike '%s')
                    """ %(context['con_fiscalyear_id'],'03%','06%','09%','12%')
        if context.get('con_period_unit_start', False) and context['con_period_unit_start'] =='qtr':
            if context.get('con_fiscalyear_id', False):
                sql = """
                    select id from account_period
                    where fiscalyear_id = %s
                    and (code ilike '%s' or code ilike '%s' or code ilike '%s' or code ilike '%s')
                    """ %(context['con_fiscalyear_id'],'01%','04%','07%','10%')
        if sql:
            cr.execute(sql)
            period_ids = [r[0] for r in cr.fetchall()]
            ids = self.search(cr, uid, [('id','in',period_ids)]+ args, limit=limit, context=context)
            return self.name_get(cr, uid, ids, context=context)
        return super(account_period, self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)
        
account_period()
