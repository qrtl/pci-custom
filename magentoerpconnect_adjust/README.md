Adjustments to Magento Connector
================================

This module makes adjustments to the behaviors of Magento Connector module provided by OCA.


Installation
============

No installation steps required other than installing the module itself.


Configuration
=============

- Boolean field 'Default Magento Salesperson' is added in user master.  'Sales Manager' group has access rights to this field.  One user should be selected as the default salesperson for Magento sales orders, who should be set as the salesperson of the sales order imported from Magento in case there is no salesperson assigned in customer master.
- Boolean field 'Magento Tax Exempt' is added in fiscal position master.  One fiscal position should be selected as the "tax exempt" fiscal position which should be set to customer master imported from Magento in case the customer's address (state) is not 'CA'.


Usage
=====

Let Magento Connector do the job of creating customers and sales orders as normal.

