import SalesOrderHTTPS
from SalesOrderTools import EventFactory
import SalesOrderDAO

shopifyApi = SalesOrderHTTPS.ShopifyApiHelper()
factory = EventFactory(shopifyApi, 0, True)


## Wait for this code to run as it takes a while to build an order database from a large shopify store
factory.buildOrderDatabase()
