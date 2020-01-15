# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'US Check Printing Adjustments',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Localization',
    'license': "AGPL-3",
    'summary': 'Print US Checks',
    'description': """
This module will add the partner's address to the "Print Check (Top)" report.
    """,
    'depends': ['l10n_us_check_printing'],
    'data': [
        'report/print_check.xml',
    ],
    'installable': True,
    'auto_install': False,
}
