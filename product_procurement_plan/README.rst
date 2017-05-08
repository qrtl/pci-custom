Procurement Info Update
=======================

* Adds fields in product master.
  * Average Qty Needed (Calculated)
  * Adjusted Qty <- optional - only show in case manual adjustment is allowed
  * Average Qty Needed (Adjusted) <- optional - only show in case manual adjustment is allowed
  * Procurement Lead Time (Calculated)
  * Procurement Lead Time (Manual)
* Adds a menu item to open a wizard to run procurement info update. ('Warehouse > Products > Product Proc. Info Update')
* Adds a menu item to show product with procurement info in list view. ('Warehouse > Products > Product Proc. Info')


Installation
============

No installation steps required other than installing the module itself.


Configuration
=============

* A new boolean field is added in `Warehouse` configuration screen to indicate whether manual adjustments to needed quantities are allowed.  The optional fields in product master should show if this field is selected.
* A field `Number of months to consider in Product Proc. Info Update` is added in company.  Default value is `6`.  Adjust the value as necessary.


Usage
=====

* To update procurement info, go to 'Warehouse > Products > Product Proc. Info Update' to open a wizard.
* To view the procurement info, go to 'Warehouse > Products > Product Proc. Info'.
  * This screen lets you edit `Adjusted Qty` and/or `Procurement Lead Time (Manual)`.
* For 'Suggested Stock Qty' calculation:
  * Suggested Stock Qty = Average Qty Needed [1] * Procurement Lead Time [2]
  * [1] Check in the sequence of `Avg Qty Needed (Adjusted)` > `Adjusted Qty` > `Avg Qty Needed`.
  When a qty > 0 is found, then that should be used as the Average Qty Needed.
  * [2] Check in the sequence of `Proc LT (Manu)` > `Proc LT (Calc)`.
  When a value > 0 is found, then that should be used as the Procurement Lead Time.
