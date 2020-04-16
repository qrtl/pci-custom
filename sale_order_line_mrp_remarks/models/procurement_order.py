# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    def _prepare_mo_vals(self, bom):
        res = super(ProcurementOrder, self)._prepare_mo_vals(bom)
        proc = self
        while proc:
            if proc.move_dest_id and \
                    proc.move_dest_id.raw_material_production_id:
                res['remarks'] = \
                    proc.move_dest_id.raw_material_production_id.remarks
                break
            elif proc.sale_line_id:
                res['remarks'] = proc.sale_line_id.remarks
                break
            elif proc.move_dest_id:
                proc = proc.move_dest_id.procurement_id
            else:
                proc = False
        return res
