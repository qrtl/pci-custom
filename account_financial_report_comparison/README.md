Account Financial Report Comparison
===================================

This module adds report functions to print B/S and P&L for various selection criteria and formats.

The purpose of this is to extend the capabilities of OpenERP's abilities to report accounting and finances. By default OpenERP can export reports based on international accounting and financial standards, but the United States needs further options to allow easy reporting.


Installation
============

This module depends on Aeroo Reports.  Make sure that you have installed `report_aeroo` and `report_aeroo_ooo` from this repository before installing this module.


Configuration
=============

No special configuration is required.


Usage
=====

Following menu items should be added upon installation of this module:

- 'Accounting > Reporting > Legal Reports > Accounting Reports > Balance Sheet(Multi-Period)`
- 'Accounting > Reporting > Legal Reports > Accounting Reports > Profit and Loss(Multi-Period)`
- 'Accounting > Reporting > Legal Reports > Accounting Reports > Profit and Loss(Analytic-Accounts)`

Clicking on the menu item should open a wizard in which you should select your reporting criteria.  Output should be downloaded to a `.xls` file upon running the report.

