This module does the following:

* Adds fields in the product model.

  * Average Qty (Calculated)
  * Average Qty (Manual)
  * Average Qty (Adjusted)
  * Lead Time (Calculated)
  * Lead Time (Manual)
  * Lead Time (Adjusted)
  * Suggested Stock Quantity
  * Variance

* Adds a menu item to open a wizard to run procurement info update.
* Adds a menu item to show product with procurement info in list view.
  (*Inventory > Inventory Control > Product Proc. Info*)

The goal of this module is to facilitate the procurement decision making by calculating
the suggested stock quantity (based on the past transactions and the relevant master
settings) and the variance from the current on-hand stock the incoming qty.

Average Quantity Calculation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The average quantity calculation is done based on number of top-node products shipped
to the customer in a given period. The program first identifies the top-node products
for the selected products (based on the BOM structure), summarizes the shipped
quantities, and then calculates the used quantities of the components (based on the
BOM structure).

Procurement Lead Time Calculation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The procurement lead time of each product is calculated with the following strategy.

* Purchased products: Based on the actual lead time from the purchase order confirmation
  to the receipt (for physical products) or to the vendor bill (for services) for the
  given period.
* Manufactured products: Manufacturing Lead Time of the product + procurement lead time
  of the components (pick the longest lead time at each node to accumulate).

Suggested Stock Quantity and Variance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Suggested Stock Quantity = Average Qty (Adj) * Lead Time (Adj)
* Variance = Quantity On Hand + Incoming - Suggested Stock Quantity
