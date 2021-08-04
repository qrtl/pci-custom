# -*- coding: utf-8 -*-
# Copyright 2017 Pledra
# Copyright 2018 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # this overrides the method in product_configurator module
    def validate_domains_against_sels(self, domains, sel_val_ids):
        # process domains as shown in this wikipedia pseudocode:
        # https://en.wikipedia.org/wiki/Polish_notation#Order_of_operations
        stack = []
        for domain in reversed(domains):
            if type(domain) == tuple:
                # evaluate operand and push to stack
                if domain[1] == "in":
                    if not set(domain[2]) & set(sel_val_ids):
                        stack.append(False)
                        continue
                else:
                    if set(domain[2]) & set(sel_val_ids):
                        stack.append(False)
                        continue
                stack.append(True)
            else:
                # evaluate operator and previous 2 operands
                # compute_domain() only inserts 'or' operators
                # compute_domain() enforces 2 operands per operator
                operand1 = stack.pop()
                operand2 = stack.pop()
                stack.append(operand1 or operand2)

        # # 'and' operator is implied for remaining stack elements  # QTL del
        # avail = True  # QTL del
        # while stack:  # QTL del
        #     avail &= stack.pop()  # QTL del
        # return avail  # QTL del

        # return True if value is available according to any of the  # QTL add
        # restrictions  # QTL add
        avail = True  # QTL add
        if stack and True not in stack:  # QTL add
            avail = False  # QTL add
        return avail  # QTL add
