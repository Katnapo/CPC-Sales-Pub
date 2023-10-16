from flask import Flask, Response
import atexit
import time
from apscheduler.schedulers.background import BackgroundScheduler
import SalesOrderHTTPS
from SalesOrderTools import EventFactory
import SalesOrderDAO
import Constants

app = Flask(__name__)

""" Establish the API singleton and the event factory (i.e the instance that receives events from Shopify and
    processes them)  """

shopifyApi = SalesOrderHTTPS.ShopifyApiHelper()
factory = EventFactory(shopifyApi, 0, True)

def eventProcessor(IDs=None, sale=None, retries=0):

    # If the event factory has processed more than 20 events, then there may be a problem. Artificially stop the
    # event processor to prevent a possible issue.
    if factory.getBatch() > 20:
        return None

    try:
        # Get the next event from the event factory. If there is no event, then the event factory will return None.
        # Two IDs are returned from the event factory. One is the previous event's ID, and the other is the current
        # This is to ensure the event factory updates the last event ID in the database.

        if retries == 0:
            IDs, sale = factory.checkForNewEvent()

    except Exception as e:
        SalesOrderDAO.setLogsToDatabase("[SO][ERROR]ShopifyPlanB", "Error in shopify event processor while using shopify tools: " + str(e))
        return None

    if sale is None:
        return None

    if sale:
        success = sale.commitAll()
        # commitAll processes the sale and sends it off to the BC instances. This function returns whether
        # the sales were pushed.

        if success:
            SalesOrderDAO.setLogsToDatabase("[SO][INFO]ShopifyPlanB", "Successfully completed sales order commit code, IDs were " + str(IDs))
        else:
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]ShopifyPlanB", "Failed to complete sales order commit code, IDs were " + str(IDs))

        factory.setBatch(1)

        # If the sales order has returned a 3 from the push function, then the sales order has failed due to a locked
        # table. This is a temporary error, therefore the program will wait 30 seconds and recurse. If the attempts
        # exceed 3, then the sales order will be sent to the failed sales order queue.

        if sale.getReason1() == 3:
            time.sleep(30)
            if retries < 3:
                sale.setRetry(2)
                eventProcessor(IDs, sale, retries + 1)

        # If all is successful, set the latest event in the database to have the latest shopify item tag.
        SalesOrderDAO.updateLatestShopifyItem(IDs[1], IDs[0])


# Reset the batch for the hour to 0, this is to prevent the program from running too fast.

def resetBatch():

    factory.resetBatch(0)

# All failed sales orders are fired through the sales orders tools.
def commitFailedSalesOrders():

    # Accountancy mode is a wear a label property - wear a label requires two sales orders to be sent to both the CPC
    # BC instance and its own WAL instance with different properties.

    # Each number triggers a different type of retry. 1 is an accountancy retry, 2 is a retry for a failed sales order
    # with cost price, and 3 is a retry for a failed sales order with sale price.

    if Constants.Constants.ACCOUNTANCY_MODE == True:
        factory.processFailedOrders(1)
        factory.processFailedOrders(2)

    else:
        factory.processFailedOrders(3)

#################################################################################


# Background scheduler for scheduling the processes of the program
scheduler = BackgroundScheduler()
scheduler.add_job(func=eventProcessor, trigger="interval", seconds=7)
scheduler.add_job(func=resetBatch, trigger="interval", hours=1)
scheduler.add_job(func=commitFailedSalesOrders, trigger="interval", hours=4)

scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@app.route("/antiSleep", methods=["POST"])
def antiSleep():
    return(Response(status=200))

@app.route("/forceCheck")
def forceCheck():
    eventProcessor()
    return "Sales Order Proceesor Flask Server. Away from this space, foul beast!"

@app.route("/forceFail")
def wsa():
    commitFailedSalesOrders()
    return "Sales Order Proceesor Flask Server. Away from this space, foul beast!"

@app.route("/")
def home():
    return "Sales Order Proceesor Flask Server. Away from this space, foul beast!"


if __name__ == "__main__":
    app.run()

