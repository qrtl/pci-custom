# -*- coding: utf-8 -*-
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Quotation Auto Confirmation",
    'version': '10.0.1.0.0',
    'license': 'LGPL-3',
    'category':'Sales',
    'description': """
- Add a cron job that will confirm "Direct Sales" quotation automatically.
    """,
    'author' : 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'depends': [
        'sale',
        'sales_team',
    ],
    'data':[
        'data/ir_cron.xml',
        'views/crm_team_views.xml',
    ],
}
