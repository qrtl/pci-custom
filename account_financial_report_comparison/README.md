Enabling physical inventories with a past date
==============================================

Follow below steps for the preparation of applying bug fix/enhancement on physical inventories.

1. Stop OpenERP.
2. Replace `addons/stock/stock.py` with the `stock.py` file from the GitHub repository.
3. Restart OpenERP.
4. Install `stock_physical_inventory_adjust`.


Changes Made to OpenERP By This Extension
=========================================

1. `Creation Date`
  - This date will have no substantial impact for stock move an journal entry records. Please use this date just for reference.

2. `Date Done`
  - At `Confirm Inventory` OpenERP does following calculation to generate stock move records:
    - (`Quantity` in `General Information` tab) &minus; (`Quantity` as of `Date Done`)
  - At `Validate Inventory` the `Date Done` value is used as the effective date for stock moves and associated journal entry.


Some Points to Note
===================

1. When one presses `Fill Inventory`, OpenERP populates `General Information` tab with products and quantities. The info is based on the current OpenERP inventory, not the inventory as of `Creation Date` or `Date Done`. <strong>This is the default behavior of OpenERP.</strong>

2. When one presses `Validate Inventory`, OpenERP generates a journal entry while changing the status of stock moves to `Done`. However, when one presses `Cancel Inventory`, OpenERP does not cancel the corresponding journal entry. <strong>This is a bug, but is on the roadmap to be fixed. Please, remember to delete the journal entry if `Cancel Inventory` is used.</strong>

3. Since we have modified the original `stock.py` file, if one updates OpenERP, depending on the latest source code changes to the `stock.py` file, the changes will need to be merged.

