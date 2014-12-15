# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging

class account_account(osv.osv):
    _inherit = "account.account"
    _columns = {
       'reports': fields.boolean(u'Customer Sales Report'),
       'sp': fields.char(u'3123123 Sales Report'),
    }
account_account()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
