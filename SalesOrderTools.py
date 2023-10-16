from SalesOrderObject import ShopifyEvent
import time
import SalesOrderDAO
import Constants

class EventFactory:

    def __init__(self, shopifyApiObj, count, debug=True):

        self.debug = debug
        self.count = count
        self.ShopifyApiObj = shopifyApiObj

    # This is used at the beginning of the project only. Get all existing orders to make an up to date version of the
    # database, then allowing whichever order is next to be taken. Code is working fine as of 24/04/2022

    def getShopifyEventByPreviousId(self, previousOrderId, first=False):

        # If first is true (Only when starting the project from scratch should first be true) the first entry in
        # wear a label will be taken
        resource_point = "events.json"

        # TODO: LOOK INTO THE CONSEQUENCES OF USING THE VERB CONFIRMED
        if first == True:
            event = self.ShopifyApiObj.constructShopifyGetRequest(resource_point, [["filter", "Order"], ["limit", "1"],
                                                                               ["verb", "confirmed"]])
        else:
            event = self.ShopifyApiObj.constructShopifyGetRequest(resource_point,
                                                                  [["since_id", str(previousOrderId)], ["filter", "Order"],
                                                            ["limit", "1"], ["verb", "confirmed"]])

        # Dissect the shopify get request - json dictionary key starts with "events"
        try:
            event = event.json()
            event = event["events"]
            
        except Exception as e:
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]FailedToGetEvent", "Failed to get/dissect event from shopify (previous ID) - error was: " + str(e))
            return []
        
        # If an empty list is found, return an empty list in turn.
        if not event:
            return []

        # The return list is one layer in, since were only grabbing the order after the first list entry works.
        # The first argument of the return list needs to be formatted to remove its # otherwise MYSQL will say no.
        event = event[0]
        
        # TODO: LOOK AT WHETHER AN EVENT OBJECT IS NECCESARY
        
        return [int((event["arguments"][0]).replace("#", "")), int(event["id"]),
                int(event["subject_id"]),
                event["created_at"], (event["message"]), 0, 0, 0, 0]

    # I dont believe this code is used anywhere, its simply for debugging...
    def getShopifyEventById(self, eventId):

        resource_point = "REDACTED" + str(eventId) + ".json"

        event = self.ShopifyApiObj.constructShopifyGetRequest(resource_point)
        try:
            event = event.json()
            event = event["event"]
            
        except Exception as e:
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]FailedToGetEvent", "Failed to get/dissect specific event from shopify - error was: " + str(e))
            return []

        return [int((event["arguments"][0]).replace("#", "")), int(event["id"]),
                int(event["subject_id"]),
                event["created_at"], (event["message"]), 0, 0, 0, 0]

    def buildOrderDatabase(self):

        # Developer tool - not made particualrly for production use.


        # Only time where first is true here. Gets the first event to then be used.
        firstEvent = self.getShopifyEventByPreviousId(0, True)
        print(firstEvent)

        # Not failed will change to false in the while loop if there is a faliure
        notfailed = True
        manylist = []

        while notfailed:

            # Get the id from the previous event, 0.5001 is there for API usage limits, realprevious is
            # groomed to be added to the database while its data is used to grab the next item to be groomed.
            try:
                nextid = firstEvent[1]
                time.sleep(0.5001)
                realprevious = firstEvent
                realprevious[5] = 1
                realprevious[6] = 0
                realprevious[8] = 1
                firstEvent = self.getShopifyEventByPreviousId(nextid, False)
                manylist.append(realprevious)
                print(realprevious)
                continue

            except Exception as e:
                print(e)
                notfailed = False

        # Give the last item of the list the 1 to signify its the last item added to the database.
        manylist[len(manylist) - 1][6] = 1

        SalesOrderDAO.setAllShopifyOrders(manylist)

    # Check if there's a new item for the database.
    def checkForNewEvent(self):

        # Get the latest event recorded by the database.
        latestDatabaseEvent = SalesOrderDAO.getLatestShopifyItem()

        #if self.debug:
        #    databaseHandler.setLogsToDatabase("[SO][DEBUG]GotLatestEventFromDB",
        #                                       "Fetched the latest event from database")

        if latestDatabaseEvent is None:

            # TODO: MAKE THE WARNING HERE MORE SEVERE - AKA EMAILS
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]NoLatestEventPointer",
                                               "There was no last_item record found... perhaps manual modifications were made?")
            return None, None

        # Use the Shopify event to get the next item after the one existing
        try:
            latestEvent = self.getShopifyEventByPreviousId(latestDatabaseEvent[1], False)

        except Exception as e:
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]GotLatestEventFromShopify",
                                               "Failed to fetch latest shopify event - error was: " + str(e))
            return None, None

        # If no next item is found, latestEvent will be empty warranting no action.
        if not latestEvent:
            return None, None

        # If the items are the same, dont do anything
        # This likely will never trigger again but was caused by a rare bug I kept coming across.
        if int(latestEvent[2]) == int(latestDatabaseEvent[2]):
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]IdenticalItems",
                                               "Identical items were found somehow? Records were (External event and db event): "
                                            + str(latestEvent) +
                                               " and " + str(latestDatabaseEvent))
            return None, None

        # Supplying everything else doesnt happen, take action. Return the IDs of the latest event from shopify and
        # the latest event from the database for comparison. Also return the latest shopify event.
        else:
            return [latestEvent[2], latestDatabaseEvent[2]], ShopifyEvent(self.ShopifyApiObj,
                                                                          latestEvent)

    def processFailedOrders(self, type):

        try:
            # Goes to the database and finds all instances of a order that failed to push.
            if type == 1:
                dbEventList = SalesOrderDAO.getAllShopifyAccountancyFaliures()
            else:
                dbEventList = SalesOrderDAO.getAllShopifyItemFaliures()

            print(dbEventList)
            if self.debug:
                SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]GetAllPostingFaliures",
                                                   "Got all posting faliures successfully.")
        except Exception as e:
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]GetAllPostingFaliures",
                                               "Failed to get posting errors. Error was " + str(e))
            return None

        if dbEventList is None:
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]GetAllPostingFaliures",
                                               "No posting faliures found")
            return None

        if not isinstance(dbEventList, list):
            dbEventList = [dbEventList]

        for event in dbEventList:

            # For each event, if the number of events is bigger than 5, it is not the last item and it has not been pushed,
            # delete it from the database.
            # Change the first number for debugging. Starting number is 5.
            if Constants.Constants.ACCOUNTANCY_MODE:
                if (event[7] > Constants.Constants.RETRY_THRESHOLD and event[6] == 0) and (event[5] == 0 or event[8] == 0):
                    SalesOrderDAO.deleteShopifyRecord(event[1])
                    SalesOrderDAO.setLogsToDatabase("[SO][WARN]DeletedFailedItem",
                                                       "Deleted item that failed to post to BC. Item was order number: " + str(
                                                           event[0]))
                    return None
            else:
                if (event[7] > Constants.Constants.RETRY_THRESHOLD and event[6] == 0) and (event[5] == 0):
                    SalesOrderDAO.deleteShopifyRecord(event[1])
                    SalesOrderDAO.setLogsToDatabase("[SO][WARN]DeletedFailedItem",
                                                       "Deleted item that failed to post to BC. Item was order number: " + str(
                                                           event[0]))
                    return None


            try:

                # Shopify event object is created from event in for loop if test above is passed. Commit this object without
                # a new row in the database
                salesObj = ShopifyEvent(self.ShopifyApiObj, list(event), type)

                salesObj.pushFailedOrder()
                if self.debug:
                    SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]PostedFailedItem",
                                                       "Processing of failed item ended. Item was: " + str(event))
            except Exception as e:
                SalesOrderDAO.setLogsToDatabase("[SO][ERROR]PostedFailedItem",
                                                   "Failed the processing of failed items. Error was " + str(e))

    def setBatch(self, value):

        self.count = self.count + value

    def getBatch(self):

        return self.count

    def resetBatch(self, value):

        self.count = value
