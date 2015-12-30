Account Batch Invoice Payment
=============================

This module adds following functions:

- Invoices related to sales orders whose `order_policy` ("Create Invoice") is NOT `manual` ("On Demand") will not be processed by this function.
- Invoice should have only one origin sales order to be processed by this function.

Installation
============

Just install the module.  This module depends on `shipment_day` module.


Configuration
=============



Usage
=====

