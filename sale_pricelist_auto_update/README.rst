.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

==============================
Auto Update Customer Pricelist
==============================

This module adds the function to automatically update customers' pricelist
assignment based on their purchases of the current/last year.

Configuration
=============

Following points need to be configured before starting to use the function:

* Go to *Technical > Date ranges > Date Range Types*, and create a record with 
  "Fiscal Year" selection.
* Go to *Technical > Date ranges > Date Ranges*, and create records with the
  type whose "Fiscal Year" is selected.  Range should be 1st January through
  31st December of the year.
* Go to *Sales > Configuration > Pricelists > Pricelist Groups*, and create
  records that group multiple pricelists.
* Go to *Sales > Configuration > Pricelists > Pricelists*, and set "Sale
  Threshold Amount" and "Pricelist Group" for relevant pricelists.
* Select "Shipping Cost" in product form for those that need to be excluded
  from sales amount calculation.

Usage
=====

The function performs the following when sales order is created/updated:

* Recalculate the sales amount of the year (excl. delivery charges) based on
  the order date.
* Update the pricelist of the customer based on the sales amounts of the
  current year and last year (consider the higher amount).

There is also a wizard to perform above for all the customers at once at
*Sales > Configuration > Pricelists > Reset Customer Pricelist*.

* The beginning of each year, the wizard should be run with last year's
"Date Range", e.g. start of 2019 should select 2018 as "Data Range", hence 
every customers' 2018 yearly sales will be recomputed and the pricelist will
be updated accordingly.
