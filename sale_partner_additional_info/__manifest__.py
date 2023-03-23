# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Partner Additional Information",
    "version": "10.0.1.0.0",
    "category": "Sales",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "website": "https://www.quartile.co",
    "depends": ["sale"],
    "data": [
        "views/res_partner_views.xml",
        "reports/additional_info_templates.xml",
        "reports/invoice_report_templates.xml",
        "reports/sale_report_templates.xml",
    ],
    "installable": True,
}
