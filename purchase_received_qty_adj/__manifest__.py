# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Showing actual received quantity of Purchase Order',
    'version': '10.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Purchase',
    'license': "LGPL-3",
    'description': """
- Add new field qty_received_net
- Computes the actual quantity received that excluding the quantity in
return orders
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
