## -*- coding: utf-8 -*-
%for inv in objects :
<%def carriage_returns(text):
    return text.replace('\n', '<br />')
%>
<% setLang(inv.partner_id.lang) %>
<html>
    <head>
        <style type="text/css">
            ${css}
            html,body{font-family:helvetica; font-size:12;width:100%;margin:0;padding:0;}
            table {width: 100%; page-break-after:auto; border-collapse: collapse; cellspacing:0; font-size:12px;}
            .clear{clear:both;}
            .section{margin:10px 0 10px 0; width:100%;}
            .invoice-head-company,.invoice-head-company>table{display:inline-block; float:left;}
            .invoice-head-info,.invoice-head-info>table{display:inline-block; float:right;}
            .invoice-state{text-align:center; text-transform:uppercase; color:red; font-size:50px; margin-top:0; margin-bottom:0;}
            .invoice-address th{width:50%;}
            .tabledata td{ margin: 0px; padding: 3px; border: 1px solid #E3E3E3;  vertical-align: top; }
            .tabledata th { margin: 0px; padding: 3px; border: 1px solid Grey;  vertical-align: top; }
            .note {font-size:75%}
        </style>
    </head>
    <body>
        <div class="invoice-head section">
            <div class="invoice-head-company">
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
            <div class="invoice-head-info">
                <table>
                    <tr>
                        <td>
                            <h2>
                                %if inv.type == 'out_invoice' :
                                    ${_("Customer Invoice")} 
                                %elif inv.type == 'in_invoice' :
                                    ${_("Supplier Invoice")} 
                                %elif inv.type == 'out_refund' :
                                    ${_("Credit Memo")} 
                                %elif inv.type == 'in_refund' :
                                    ${_("Supplier Refund")} 
                                %endif
                            </h2>
                        </td>
                        <td>
                            <h2>${_(": ")}${inv.number or ''|entity}</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h2>${_("Invoice Date")}</h2>
                        </td>
                        <td>
                            <h2>${_(": ")}${formatLang(inv.date_invoice, date=True)|entity}</h2>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            %if inv.state in ['proforma','proforma2']:
                                <h1 class="invoice-state">${_("ProForma")}</h1> 
                            %endif
                            %if inv.state in ['cancel','paid']:
                                <h1 class="invoice-state">
                                    ${inv.state}
                                    %if inv.state == 'paid':
                                        &#x270c;
                                    %endif
                                </h1> 
                            %endif
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="clear"></div>
        <div class="invoice-address section tabledata">
            <table>
                <tr>
                    <th>
                        ${_("Billing Address")}
                    </th>
                    <th>
                        ${_("Shipping Address")}
                    </th>
                </tr>
                <tr>
                    <td>
                        ${inv.partner_id.address_label|carriage_returns}
                    </td>
                    <td>
                        ${inv.address_shipping_id.address_label|carriage_returns}
                    </td>
                </tr>
            </table>
        </div>
        <div class="invoice-customer section tabledata">
            <table >
                <tr>
                    %if inv.name :
                        <th>${_("Customer Ref")}</th>
                    %endif
                    %if not inv.picking_ids and inv.origin:
                        <th>${_("Origin")}</td>
                    %endif
                    %if inv.picking_ids:
                        <th>${_("Pickings/Order")}</th>
                    %endif
                    %if inv.reference:
                        <th>${_("Reference")}</th>
                    %endif
                    <th >${_("Payment Term")}</th>
                    <th >${_("Due Date")}</th>
                    <th>${_("Curr")}</th>
                </tr>
                <tr>
                    %if inv.name :
                        <td>${inv.name.rfind(':') > 0 and inv.name[:inv.name.rfind(':')] or inv.name}</td>
                    %endif
                    %if not inv.picking_ids and inv.origin:
                        <td>${inv.origin} </td>
                    %endif
                    %if inv.picking_ids:
                        <td style="padding:0px;">
                            <table style="border:none;">
                                %for pick in inv.picking_ids:
                                    <tr style="border:none">
                                        <td style="border:none">${pick.name} / ${formatLang(pick.date, date=True)|entity}</td>
                                        %if pick.sale_id:
                                            <td style="border:none">${pick.sale_id.name} / ${formatLang(pick.sale_id.date_order, date=True)|entity}</td>
                                        %endif
                                    </tr>
                                %endfor
                            </table>
                        </td>
                    %endif
                    %if inv.reference :
                        <td>${inv.reference}</td>
                    %endif
                    <td>${inv.payment_term.name or ''}</td>
                    <td>${inv.date_due or ''}</td>
                    <td>${inv.currency_id.name}</td>
                </tr>
            </table>
        </div>
        <div class="invoice-body section tabledata">
            <table>
                <thead>
                    <tr style=" border-width:1px; border-style:solid;">
                        %if inv.print_code:
                            <th>${_("SKU")}</th>
                        %endif
                        <th>${_("Item")}</th>
                        %if inv.print_ean:
                            <th>${_("EAN")}</th>
                        %endif
                        %if inv.print_serial_id:
                            <th>${_("Serial")}</th>
                        %endif
                        <th>${_("Taxes")}</th>
                        <th>${_("QTY")}</th>
                        <th>${_("Unit")}</th>
                        <th>${_("Unit Price")}</th>
                        %if inv.print_price_unit_id == True:
                            <th>${_("Price/Unit")}</th>
                        %endif
                        %if inv.amount_discount != 0:
                            <th>${_("Disc.(%)")}</th>
                        %endif
                        <th>${_("Price")}</th>
                    </tr>
                </thead>
                <tbody>
                    <%shipping=0.00%>
                    %for line in inv.invoice_line_sorted :
                        %if line.product_id.default_code=="SHIP":
                            <%
                                shipping=line.price_subtotal
                                continue
                            %>
                        %endif
                        <tr>
                            %if inv.print_code:
                                <td>${line.product_id.default_code or ''|entity}</td>
                            %endif
                            <td>
                                 %if line.product_id :
                                    ${line.product_id.name |entity}
                                %else :
                                    ${line.name|entity}
                                %endif
                                <br/>
                                %if line.note > 0 :
                                    ${line.note |carriage_returns}
                                %endif
                            </td>
                            %if inv.print_ean:
                                <td>${line.product_id.ean13 or ''}</td>
                            %endif
                            %if inv.print_serial_id:
                                <td>${line.serial_id.name or ''}</td>
                            %endif
                            <td>${ ', '.join([ tax.name or '' for tax in line.invoice_line_tax_id ])|entity}</td>
                            <td style="white-space:nowrap;text-align:right;">${formatLang(line.quantity,digits=2)}</td>
                            <td style="white-space:nowrap;text-align:left;">${line.uos_id.name or _("Unit")}</td>
                            <td style="white-space:nowrap;text-align:right;">${formatLang('price_unit_pu' in line._columns and line.price_unit_pu or line.price_unit,digits=2,currency_obj=inv.currency_id)}</td>
                            %if inv.print_price_unit_id == True:
                                <td style="white-space:nowrap;text-align:left;">${line.price_unit_id.name or ''}</td>
                            %endif
                            %if inv.amount_discount != 0:
                                <td style="white-space:nowrap;text-align:right;">${line.discount or 0.00}</td>
                            %endif
                            <td style="white-space:nowrap;text-align:right;">${formatLang(line.price_subtotal,digits=2,currency_obj=inv.currency_id)}</td>
                        </tr>
                    %endfor
                        <tr>
                            <td colspan="${inv.cols}" style="border-style:none"/>
                            <td style="border-top:2px solid;white-space:nowrap"><b>${_("Net Total")}:</b></td>
                            <td style="border-top:2px solid;text-align:right">${formatLang(inv.amount_untaxed-shipping,digits=2,currency_obj=inv.currency_id)}</td>
                        </tr>
                        <tr>
                            <td colspan="${inv.cols}" style="border-style:none"/>
                            <td><b>${_("Shipping")}:</b></td>
                            <td style="text-align:right">${formatLang(shipping,digits=2,currency_obj=inv.currency_id)}</td>
                        </tr>
                        <tr>
                            <td colspan="${inv.cols}" style="border-style:none"/>
                            <td ><b>${_("Taxes")}:</b></td>
                            <td style="text-align:right">${formatLang(inv.amount_tax,digits=2,currency_obj=inv.currency_id)}</td>
                        </tr>
                        <tr> 
                            <td colspan="${inv.cols}" style="border-style:none"/>
                            <td style="border:2px solid;font-weight:bold;white-space:nowrap">${_("Total")}:</td>
                            <td style="border:2px solid;text-align:right;font-weight:bold">${formatLang(inv.amount_total,digits=2,currency_obj=inv.currency_id)}</td>
                        </tr>
                        %if inv.residual < inv.amount_total and inv.state not in ['draft']:
                            <tr>
                                <td colspan="${inv.cols}" style="border-style:none" />
                                <td style="border:2px solid;font-weight:bold;white-space:nowrap">${_("Payment(s)")}:</td>
                                <td style="border:2px solid;text-align:right;font-weight:bold">${formatLang(inv.amount_total-inv.residual,digits=2,currency_obj=inv.currency_id)}</td>
                            </tr>
                            <tr>
                                <td colspan="${inv.cols}" style="border-style:none" />
                                <td style="border:2px solid;font-weight:bold;white-space:nowrap">${_("Total Due")}:</td>
                                <td style="border:2px solid;text-align:right;font-weight:bold">${formatLang(inv.residual,digits=2,currency_obj=inv.currency_id)}</td>
                            </tr>
                        %endif
                </tbody>
            </table>
        </div>
        %if inv.comment:
            <div class="section tabledata">
                <table>
                    <tr>
                        <th>Additional Notes</th>
                    </tr>
                    <tr>
                        <td>
                            ${inv.comment|carriage_returns}
                        </td>
                    </tr>
                </table>
            </div>
        %endif:
        <p style="page-break-after:always"></p>
    </body>
</html>
%endfor