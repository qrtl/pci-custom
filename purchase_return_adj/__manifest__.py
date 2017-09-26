# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Update receive qty of Purchase Order after return',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Purchase',
    'license': "LGPL-3",
    'description': """
- Add new field qty_received_adj which holds the quantity received excluding
quantity in return orders.
- Add transfer reference to stock move tree view
""",
    'depends': [
        'purchase',
        'purchase_stock_picking_return_invoicing',
    ],
    'data': [
        'views/purchase_order_view.xml',
        'views/stock_move_view.xml',
    ],
    'installable': True,
}
