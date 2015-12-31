==================
Sale Batch Confirm
==================

This module adds following functions:
- Adds parameter fields in Shop (`sale.shop`) for batch confirmation of quotations
- Adds a scheduled action to process batch confirmation of quotations
- Adds menu item `Sales > Sales > Confirm Sales Quotations` which opens a wizard to batch confirm quotations


Installation
============

Just install the module.  This module depends on `shipment_day` module.


Configuration
=============

- In `Sales > Configuration> Sales > Shop`, set following values as necessary for relevant shops:
  - `Shipment Day`: set the shipment day which is used for shipment date proposal
  - `Confirm SO by Scheduled Action`: select if quotations with the shop should be auto-confirmed by scheduled action
  - `Default Shop in SO Confirmation Wizard`: select if the shop should be proposed in the wizard (only one shop should have this field selected)  
- Adjust `Next Execution Date` of `Batch Confirm Quotations` record in `Settings > Technical Scheduler > Scheduled Actions` according to business needs. 
- Note that timezone for the superuser should be set according to the business location as it is used in identifying today's date.


Usage
=====

Under normal circumstances, let the scheduled action do the job of confirming quotations once a week.

If quotations need to be confirmed at an irregular timing for some reason (e.g. shipment date needs to be made earlier due to holiday), user can manually run the function to batch confirm quotations through the wizard.
