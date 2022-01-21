The function performs the following when sales order is created/updated:

* Recalculate the sales amount of the year (excl. delivery charges) based on
  the order date.
* Update the pricelist of the customer based on the sales amounts of the
  current year and last year (consider the higher amount).

There is also a wizard to perform above for all the customers at once at
*Sales > Configuration > Pricelists > Reset Customer Pricelist*.

The beginning of each year, the wizard should be run with last year's
"Date Range", e.g. start of 2019 should select 2018 as "Date Range", hence
every customers' 2018 yearly sales will be recomputed and the pricelist will
be updated accordingly.
