# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Spec Sheet Report Py3o',
    'version': '10.0.1.0.1',
    'category': 'Manufacturing',
    'license': 'AGPL-3',
    'summary': 'py3o spec sheet report',
    'description': """
Spec Sheet Report Py3o
===================

This module adds a py3o spec sheet report.

    """,
    'author': 'Quartile Limited',
    'depends': [
        'report_py3o',
        'mrp',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_special_tag_views.xml',
        'views/product_template_views.xml',
        'views/mrp_production_views.xml',
        'report.xml',
    ],
    'installable': True,
}
