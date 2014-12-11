# -*- encoding: utf-8 -*-

{
    'name': 'PCI Account Report',
    'version': '1.0',
    "category" : "Generic Modules/Sales & Purchases",
    'description': """
     """,
    'author': 'OSCG',
    'depends': ['base','account','sale_journal','report_aeroo_ooo','report_aeroo'],
    'init_xml': [],
    'update_xml': [
       'wizard/pl_customer_view.xml',
        'pl_customer_report.xml',
        'pl_account.xml',
    ],
   
    'demo_xml': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
