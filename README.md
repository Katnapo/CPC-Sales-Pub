WAL-Sales-Orders

*** 

Wear a label integration work, specifically to do with sales orders.

***

This service was in use for multiple Shopify platforms between 2022 into 2023. It was used to format and send shopify orders to Childsplay's ERP system.

I consider this service to be better structred than the stock sync and item upload code, although as time went on and more caveats to how sales orders were handled were introduced, certain sections became bloated (See where it posts sales orders, there are a few different ways of doing this due to new accountancy rules set after the creation of the service).

***
A brief overview:

Shopify would send out a notification to the flask service via webhook subscription to wake it.
The service checks for any order younger than its most recent edition to the database.
If a younger order is found, send the order to the ERP system / other caveat functionality like send an email if item is marked as damaged.
Store the order in the database, if a 200 is not returned from the ERP system then mark that item in the database as failed.
A sweeper service picks up any failed items.

Overall, the file structure is alot more obvious than its counterparts; You will find the main functionality in the app, SalesOrderTools and SalesOrderObject.