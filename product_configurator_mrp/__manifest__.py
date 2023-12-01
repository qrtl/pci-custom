# -*- coding: utf-8 -*-
{
    'name': 'Product Configurator Manufacturing',
    'version': '10.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'BOM Support for configurable products',
    'author': 'Pledra,Quartile Limited',
    'license': 'AGPL-3',
    'website': 'https://www.quartile.co',
    'depends': [
        'mrp',
        'product_configurator'
    ],
    "data": [
        'security/configurator_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
