Account Batch Invoice Payment
=============================

This module adds following functions:
- Adds parameter fields in Shop (`sale.shop`) for batch processing customer invoice validation and payments
- Adds a scheduled action to batch process invoice validation and payments
- Adds menu item `Accounting > Customers > Validate Invoice & Pay` which opens a wizard to batch process invoice validation and payments

Assumptions:
- Only draft invoices related to sales orders with all of the following conditions will be processed by this function:
  - `order_policy` ("Create Invoice") is `manual` ("On Demand")
  - Payment Method is set
  - Shop is selected for processing (either in shop master for scheduled job or in the wizard)
  - Scheduled Time of the related DO is on or before the Threshold Date
- Invoice should have only one origin sales order to be processed by this function.


Installation
============

Just install the module.  This module depends on `shipment_day` and `connector_ecommerce` modules.


Configuration
=============

- In `Sales > Configuration> Sales > Shop`, set following values as necessary for relevant shops:
  - `Shipment Day`: set the shipment day which is used for shipment date proposal
  - `Validate & Pay Invoices by Scheduled Action`: select if draft invoices related to SO's with the shop should be auto-validated and paid by scheduled action
  - `Default Shop in Invoice & Payment Wizard`: select if the shop should be proposed in the wizard (only one shop should have this field selected)  
- Adjust `Next Execution Date` of `Batch Process Invoices` record in `Settings > Technical Scheduler > Scheduled Actions` according to business needs. 
- Note that timezone for the superuser (expected to be used to run the scheduler) should be set according to the business location as it is used in identifying today's date.


Usage
=====

Under normal circumstances, let the scheduled action do the job of validating and paying invoices of given criteria once a week.

If the process needs to be run at an irregular timing for some reason (e.g. shipment date needs to be made earlier due to holiday), user can manually run the function to batch process invoice validation and payments through the wizard.
