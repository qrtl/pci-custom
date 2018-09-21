# -*- coding: utf-8 -*-
# © 2017 Pierre Faniel
# © 2017 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock - Import Serial Numbers',
    'category': 'Warehouse',
    'summary': 'Input several serial numbers',
    'website': 'https://www.niboo.be/',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'description': '''
- Allows you to input several serial numbers instead of having to manually enter them one by one
    ''',
    'author': 'Niboo',
    'depends': [
        'stock',
    ],
    'data': [
        'wizards/serial_number_import_wizard.xml',
        'wizards/stock_config_settings.xml',
        'views/stock_picking.xml',
    ],
    'installable': True,
    'application': False,
}
