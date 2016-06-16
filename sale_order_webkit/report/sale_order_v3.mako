## -*- coding: utf-8 -*-
%for order in objects :
<%def carriage_returns(text):
    return text.replace('\n', '<br />')
%>
<% setLang(order.partner_id.lang) %>
<html>
    <head>
        <style type="text/css">
            ${css}
            html,body{font-family:helvetica; font-size:12;width:100%;margin:0;}
            table{width: 100%; page-break-inside:auto !important; border-collapse: collapse; cellspacing:0; font-size:12px;}
            .clear{clear:both;}
            .section{margin:10px 0 10px 0; width:100%;}
            .order-head-company,.order-head-company>table{display:inline-block; float:left;}
            .order-head-info,.order-head-info>table{display:inline-block; float:right;}
            .order-state{text-align:center; text-transform:uppercase; color:red; font-size:50px; margin-top:0; margin-bottom:0;}
            .order-address th{width:50%;}
            .tabledata td{ margin: 0px; padding: 3px; border: 1px solid #E3E3E3;  vertical-align: top; }
            .tabledata th { margin: 0px; padding: 3px; border: 1px solid Grey;  vertical-align: top; }
            .dontsplit { padding: 5px; page-break-inside: avoid; }
            .note {font-size:75%}
        </style>
    </head>
    <body>
        <div class="order-head section">
            <div class="order-head-company">
                <table>
                    <tr>
                        <td>${helper.embed_logo_by_name('pci_logo')|n}</td>
                    </tr>
                    <tr>
                        <td>${company.partner_id.name |entity}</td>
                    </tr>
                    <tr>
                        <td>${company.partner_id.street or ''|entity}</td>
                    </tr>
                    <tr>
                        <td>${company.partner_id.city or ''|entity}, ${company.partner_id.state_id.code or ''|entity} ${company.partner_id.zip or ''|entity}</td>
                    </tr>
                    <tr>
                        <td>Phone: ${company.partner_id.phone or ''|entity} </td>
                    </tr>
                    <tr>
                        <td>Mail: ${company.partner_id.email or ''|entity}<br/></td>
                    </tr>
                </table>
            </div>
            <% orderstate="" %>
            %if order.state == 'draft' or order.state == 'sent':
                <% orderstate="Quotation" %>
            %elif order.state == 'progress' or order.state == 'manual' or order.state == 'done':
                <% orderstate="Order" %>
            %elif order.state == 'cancel':
                <% orderstate="CANCELLED" %>
            %endif
            <div class="order-head-info">
                <table>
                    <tr>
                        <td>
                            <h2>${orderstate}${_(" N°")}</h2>
                        </td>
                        <td>
                            <h2>${_(": ")}${order.name or ''|entity}</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h2>${orderstate}${_(" Date")}</h2>
                        </td>
                        <td>
                            <h2>${_(": ")}${formatLang(order.date_order, date=True)}</h2>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="clear"></div>
        <div class="order-address section tabledata">
            <table>
                <thead>
                    <tr style=" border-width: 1px; border-style: solid; border-color: #000000;">
                        <th>
                            ${_("Billing Address")}
                        </th>
                        <th>
                            ${_("Shipping Address")}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            ${order.partner_id.address_label|carriage_returns}
                        </td>
                        <td>
                            ${order.partner_shipping_id.address_label|carriage_returns}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="order-customer section tabledata">
            <table>
                <thead>
                    <tr>
                        %if order.client_order_ref :
                            <th>${_("Your Ref")}</th>
                        %endif
                        %if order.user_id and order.user_id.name:
                            <th>${_("Salesman")}</td>
                        %endif
                        %if order.payment_term and order.payment_term.note:
                            <th>${_("Payment Term")}</th>
                        %endif
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        %if order.client_order_ref :
                            <td>${order.client_order_ref or ''}</td>
                        %endif
                        %if order.user_id and order.user_id.name:
                            <td>${order.user_id and order.user_id.name or ''}</td>
                        %endif
                        %if order.payment_term and order.payment_term.note:
                            <td>${order.payment_term and order.payment_term.note or ''}</td>
                        %endif
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="section tabledata">
            <table>
                <thead>
                    <tr>
                        <th>${_("SKU")}</th>
                        <th>${_("Item")}</th>
                        %for line in order.order_line:
                            %if show_serial(user.id):
                                <th>${_("Serial")}</th>
                                <%
                                    cols = 6
                                    break
                                %>
                            %endif
                            <%
                                cols = 5
                            %>
                        %endfor
                        <th>${_("Taxes")}</th>
                        <th>${_("QTY")}</th>
                        <th>${_("Unit")}</th>
                        <th>${_("Unit Price")}</th>
                        %for line in order.order_line:
                            %if show_discount(user.id):
                                <th>${_("Disc.(%)")}</th>
                                <%
                                    cols = cols + 1
                                    break
                                %>
                            %endif
                            <%
                                cols = cols
                            %>
                        %endfor
                        <th>${_("Price")}</th>
                    </tr>
                </thead>
                <tbody>
                    <%shipping=0.00%>
                    %for line in order.order_line :
                        %if line.product_id.default_code=="SHIP":
                            <%
                                shipping=line.price_subtotal
                                continue
                            %>
                        %endif
                        <tr>
                            <td><div class="dontsplit">${line.product_id.default_code or ''|entity}</div></td>
                            <td><div class="dontsplit">
                                %if line.product_id :
                                    ${line.product_id.name |entity}
                                %else :
                                    ${line.name|entity}
                                %endif
                            </div></td>
                            %if show_serial(user.id):
                                <td><div class="dontsplit">${line.serial_id.name or ''}</div></td>
                            %endif
                            <td><div class="dontsplit">${ ', '.join([tax.description or tax.name for tax in line.tax_id]) }</div></td>
                            <td style="white-space:nowrap;text-align:right;"><div class="dontsplit">${formatLang(line.product_uos_qty,digits=2)}</div></td>
                            <td style="white-space:nowrap;text-align:left;"><div class="dontsplit">${line.product_uos or _("Unit(s)")}</div></td>
                            <td style="white-space:nowrap;text-align:right;"><div class="dontsplit">${formatLang('price_unit_pu' in line._columns and line.price_unit_pu or line.price_unit,digits=2,currency_obj=order.currency_id)}</div></td>
                            %if show_discount(user.id):
                                <td style="white-space:nowrap;text-align:right;"><div class="dontsplit">${line.discount or 0.00}</div></td>
                            %endif
                            <td style="white-space:nowrap;text-align:right;"><div class="dontsplit">${formatLang(line.price_subtotal,digits=2,currency_obj=order.currency_id)}</div></td>
                        </tr>
                    %endfor
                        <tr>
                            <td colspan="${cols}" style="border-style:none"/>
                            <td style="border-top:2px solid;white-space:nowrap"><b>${_("Net Total")}:</b></td>
                            <td style="border-top:2px solid;text-align:right">${formatLang(order.amount_untaxed-shipping,digits=2,currency_obj=order.currency_id)}</td>
                        </tr>
                        <tr>
                            <td colspan="${cols}" style="border-style:none"/>
                            <td><b>${_("Shipping")}:</b></td>
                            <td style="text-align:right">${formatLang(shipping,digits=2,currency_obj=order.currency_id)}</td>
                        </tr>
                        <tr>
                            <td colspan="${cols}" style="border-style:none"/>
                            <td ><b>${_("Taxes")}:</b></td>
                            <td style="text-align:right">${formatLang(order.amount_tax,digits=2,currency_obj=order.currency_id)}</td>
                        </tr>
                        <tr>
                            <td colspan="${cols}" style="border-style:none"/>
                            <td style="border:2px solid;font-weight:bold;white-space:nowrap">${_("Total")}:</td>
                            <td style="border:2px solid;text-align:right;font-weight:bold">${formatLang(order.amount_total,digits=2,currency_obj=order.currency_id)}</td>
                        </tr>
                        %if order.residual < order.amount_total:
                            <tr>
                                <td colspan="${cols}" style="border-style:none" />
                                <td style="border:2px solid;font-weight:bold;white-space:nowrap">${_("Payment(s)")}:</td>
                                <td style="border:2px solid;text-align:right;font-weight:bold">${formatLang(order.amount_total-order.residual,digits=2,currency_obj=order.currency_id)}</td>
                            </tr>
                            <tr>
                                <td colspan="${cols}" style="border-style:none" />
                                <td style="border:2px solid;font-weight:bold;white-space:nowrap">${_("Total Due")}:</td>
                                <td style="border:2px solid;text-align:right;font-weight:bold">${formatLang(order.residual,digits=2,currency_obj=order.currency_id)}</td>
                            </tr>
                        %endif
                </tbody>
            </table>
        </div>
        %if order.note:
            <div class="section tabledata">
                <table>
                    <tr>
                        <th>Additional Notes</th>
                    </tr>
                    <tr>
                        <td>
                            ${order.note|carriage_returns}
                        </td>
                    </tr>
                </table>
            </div>
        %endif:
        %if order.note2:
            <div class="section tabledata">
                <table>
                    <tr>
                        <th>Additional Notes</th>
                    </tr>
                    <tr>
                        <td>
                            ${order.note2|carriage_returns}
                        </td>
                    </tr>
                </table>
            </div>
        %endif:
        <p style="page-break-after:always"></p>
    </body>
</html>
%endfor
