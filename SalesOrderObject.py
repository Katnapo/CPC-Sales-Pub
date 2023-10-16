import datetime
import time
import SalesOrderDAO
import SalesOrderHTTPS
import Constants

class ShopifyEvent:

    def __init__(self, shopifyApiObj, event, retry=0, latest=True, debug=True):

        self.shopifyApiObj = shopifyApiObj
        self.event = event
        self.order = None
        self.debug = debug
        self.latest = latest
        self.accountancy = Constants.Constants.ACCOUNTANCY_MODE
        self.postState1 = False
        self.reason1 = None
        self.postState2 = False
        self.reason2 = None
        self.retry = retry

    def handleDiscounts(self, totalDisc, l2items):

        # if the total discount is 0, return a multiplier of 1
        if float(totalDisc) == float(0):
            if self.debug:
                SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]DiscountInfoEnd",
                                                   "No discount present, therefore no process occured.")
            return float(1)

        totalSale = float(0)

        # Find the total value of the sale
        for item in l2items:
            totalSale = totalSale + float(item["price_set"]["shop_money"]["amount"])

        if self.debug:
            SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]DiscountInfoToProcess",
                                               "Discount values to be processed (total discount of all items and total sale: " + totalDisc + " and " + str(
                                                   totalSale))

        # The total amount spent is found here - this formula needs verification
        # I don't know how I wrote this, I haven't done maths since year 13
        # Karem and I tested it however and it seems to be complying.

        diff = float(totalSale) - float(totalDisc)
        finalVal = (float(100) / float(totalSale) * float(diff)) / float(100)

        if self.debug:
            SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]DiscountInfoEnd",
                                               "Discount values processed. End discount value returned was: " + str(
                                                   finalVal))

        return (float(100) / float(totalSale) * float(diff)) / float(100)
    # Gets the sales order object from shopify
    def getSalesOrder(self):

        # Try and except - if false, the order variable is still None
        try:
            self.order = self.shopifyApiObj.constructShopifyGetRequest("REDACTED" + str(self.event[2]) + ".json")
            self.order = self.order.json()
            if self.debug:
                SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]GettingShopifyOrderFromEvent",
                                                   "Got shopify order from event")
            return True
        except Exception as e:
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]GettingShopifyOrderFromEvent",
                                               "Failed to get shopify order from event - error was: " + str(e))
            return False

    def skuProcessor(self, sku, noEmail=False):

        try:
            if sku[-2:] != "-D" and sku[-2:] != "-d":
                return sku.upper()

            else:
                SalesOrderDAO.setLogsToDatabase("[SO][WARN]FoundDamagedStock",
                                                   "Found damaged stock from event in shopify - sku was: " + str(sku))
                if not noEmail:
                    import SalesOrderEmailer
                    SalesOrderEmailer.emailProcessDamagedStock(sku[:-2], self.orderNo)
                return (sku[:-2]).upper()

        except Exception as e:
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]SkuProcessing",
                                               "An error has occured while processing shopify sku - that error was: " + str(
                                                   e))
            return sku.upper()

    def orderPoster(self, doubleAccountsPost, orderlines, l1, l2ship, date):

        try:
            if doubleAccountsPost:
                self.postState2, self.reason2 = SalesOrderHTTPS.bcPostRequestSO(orderlines, [str(Constants.Constants.ACCOUNTANCY_CUSTOMER), str(l1["order_number"]), str(date),
                                                                               (str(l2ship["first_name"]) + " " + str(l2ship["last_name"])),
                                                                               l2ship["address1"], l2ship["address2"], l2ship["city"],
                                                                               l2ship["province"],
                                                                               l2ship["zip"], l2ship["country_code"]], self.account, "WAL", "v1.1", False)


            else:
                self.postState1, self.reason1 = SalesOrderHTTPS.bcPostRequestSO(orderlines, [str(Constants.Constants.MAIN_BC_CUSTOMER), str(l1["order_number"]), str(date),
                                                                               (str(l2ship["first_name"]) + " " + str(l2ship["last_name"])),
                                                                               l2ship["address1"], l2ship["address2"], l2ship["city"],
                                                                               l2ship["province"],
                                                                               l2ship["zip"], l2ship["country_code"]], [], "CPC", "v1.1", False)

        except Exception as e:
            import sys
            exception_type, exception_object, exception_traceback = sys.exc_info()
            line_number = exception_traceback.tb_lineno
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]SalesOrderPost",
                                               "Error for posting sales orders. Accounts Sales Order post = " +
                                            str(doubleAccountsPost) + " while order is: " + str(
                                                   self.event[0]) + \
                                               " with error of " + str(e) + " on line " + str(line_number))


    # Process for firing sales order at buisness central
    def postSalesOrder(self):

        import traceback
        try:

            # Checks if order variable is still unset
            if self.order is None:
                SalesOrderDAO.setLogsToDatabase("[SO][ERROR]BlankOrderObject",
                                                   "Failed to post a sales order object due to no initialization")
                return False

            # Dissects the order into different accessible levels.
            if self.debug:
                SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]OrderHandler",
                                                   "Beginning order handler. Accounts Sales Order post = " + str(self.accountancy) + " while order is: " + str(self.event[0]))



            ### PLAIN SETUP FOR EVERY SALES ORDER FROM SHOPIFY ###


            l1 = self.order["order"]
            l2ship = l1["shipping_address"]
            l2items = l1["line_items"]
            l2total = l1["total_price"]

            # Send the discount value total for all items and the list of items to find the total discounts for the item
            discount = self.handleDiscounts(l1["total_discounts_set"]["shop_money"]["amount"], l2items)

            # Takes the order number for use with the skuProcessor
            self.orderNo = l1["order_number"]

            # This list is for later - orderlines is a list of json items needed for BC post request.
            orderlines = []

            # BC requires a end date on a sales order - set for 7 days time
            today = datetime.date.today()
            next_week = today + datetime.timedelta(days=7)
            date = next_week.strftime("%Y-%m-%d")

            # Code for handling the origin of the sale. If sale tags do not include 'eBay', then the transaction is Shopify
            tags = str(l1["tags"]).split(",")

            if "eBay" in tags:
                if self.debug:
                    SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]OrderDissection",
                                                       "Event was found to originate from eBay. Setting account "
                                                       "destination to eBay. Order is: " + str(
                                                           self.event[0]))

                # This is the account found using Paul's API for BC. If replicating, ensure to call the current instance
                # of Childsplay
                account = Constants.Constants.BC_EBAY_ACCOUNT_ID

            else:
                account = Constants.Constants.BC_SHOPIFY_ACCOUNT_ID
                if self.debug:
                    SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]OrderDissection",
                                                       "Event was found to originate from shopify. Setting account "
                                                       "destination to eBay. Order is: " + str(
                                                           self.event[0]))

            # Separate blank lists created for order lines containing values we sold the products for and values
            # that the products cost us.
            sellOrderLines = []
            costOrderLines = []
            sellTotal = 0.0

            for item in l2items:

                if item["sku"] == "NOSKU":
                    continue

                # Prevent damaged stock emails on a retry sales order object, aka not 0.
                if self.retry == 0:
                    sku = self.skuProcessor(item["sku"])
                else:
                    sku = self.skuProcessor(item["sku"], True)

                vat = str(item["taxable"])

                # Sku processor has to figure out if a -D exists (signifying damaged stock) and subsequently removing
                # the -D

                print(SalesOrderHTTPS.bcGetRequest(
                    "REDACTED'" +
                    sku + "')", "N").json())
                itemId = SalesOrderHTTPS.bcGetRequest(
                    "REDACTED'" +
                    sku + "')", "N").json()["itemId"].replace(".", "")


                # Database lookup to find the cost of the sku to us. [0] at the end fetches the one item from the tuple given.
                costUs = SalesOrderDAO.getUnitCostWithSku(sku)


                # If, in the scenario there is a value of 0 in the database or None is returned, set the cost to 0
                if costUs is None or costUs == "" or costUs == False:
                    costUs = 0.0

                else:
                    costUs = costUs[0]

                if costUs == 0.0:
                    SalesOrderDAO.setLogsToDatabase("[SO][WARN]OrderDissectionUnitPrice0",
                                                       "Item in sale had a unit cost of 0. Unless item was free to "
                                                       "childsplay, confirm the unit price. Order is: " + str(
                                                           self.event[0]) + " with SKU of " + str(item["sku"]))

                # The sale price of the SKU still needs to be hit by the discount multiplier. Once this calculation is
                # complete, add it to the sale total.
                #sellUs = discount * float(item["price_set"]["shop_money"]["amount"])

                # Tax handling code, may be useful for the fushia.
                if vat == "true":
                    costUs = costUs * 1.2

                #sellTotal = sellTotal + (sellUs * int(item["quantity"]))

                # sellTotal = sellTotal + sellUs

                # Append each value for the item to its appropriate list
                # sellOrderLines.append([itemId, int(item["quantity"]), sellUs])
                costOrderLines.append([itemId, int(item["quantity"]), float(costUs)])

            # Create the account value should an accountancy entry be needed. 2D list is needed to mock the sales order
            # lines as they are also 2D and the account lines go in the same place
            sellTotal = float(l2total)
            self.account = [[account, int(1), float(sellTotal)]]


            if self.debug:
                SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]SalesOrderPost",
                                                   "Sales order posting starting. Accounts Sales Order post = " +
                                                str(self.accountancy) + " while order is: " + str(
                                                       self.event[0]))

            if self.retry == 0:
                if self.accountancy:

                    # Double account post is True, and false is for regular post but with cost lines
                    self.orderPoster(self.accountancy, orderlines, l1, l2ship, date)
                    self.orderPoster(False, costOrderLines, l1, l2ship, date)

                if not self.accountancy:

                    self.orderPoster(self.accountancy, sellOrderLines, l1, l2ship, date)

            # Will need to come back and look at this at some point. If retry is 1, attempt to redo the
            # accountancy sales order. If retry is 2, attempt to redo the cpc cost item sales order. If 3,
            # do a normal sales order

            elif self.retry == 1:

                self.orderPoster(self.accountancy, orderlines, l1, l2ship, date)

            elif self.retry == 2:

                self.orderPoster(False, costOrderLines, l1, l2ship, date)

            elif self.retry == 3:

                self.orderPoster(False, sellOrderLines, l1, l2ship, date)


            if self.debug:
                SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]SalesOrderPost",
                                                       "Sales order posting complete. Accounts Sales Order post = " +
                                                str(self.accountancy) + " while order is: " + str(
                                                           self.event[0]))

        except Exception as e:
            import SalesOrderEmailer
            SalesOrderEmailer.send_warning_mail(2, e, "Sales Order Processing, with order: " + str(self.event[0]) + " and traceback" \
                                                                                                                  " of: " + str(traceback.format_exc()))

    ## TODO: Needs a bit of refactoring here in the future, in regards to the error handling.
    def eventToDatabase(self, attempt=1):

        if self.debug:
            SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]EventToDatabasePost",
                                               "Posting attempt to database")

        time.sleep(2 ** attempt)

        if attempt == 10:
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]DBERROR",
                                               "Major database error in sales order database commit area." + str(
                                                   self.event[0]))
            self.eventToDatabase(attempt + 1)
            import emailController
            emailController.send_warning_mail(3, "Placeholder Error", "Database failed to import on 10th attempt, order number was: " + str(self.event[0]))

            time.sleep(259200)
            return False

        try:
            self.event[6] = 1
            if not self.latest:
                self.event[6] = 0
            SalesOrderDAO.setOneShopifyOrder(self.event)
            return True

        # To anyone reading, I was a bit of an idiot here. Without this try and except for database insertation,
        # there was nothing stopping the program looping over the last item in the database should the item after it
        # continuously fail being added to the database. It was the latin character of ņ that broke the database.
        # 30k sales orders were sent to buisness central within 4 days...

        except Exception as e:

            import emailController
            emailController.send_warning_mail(3, "Database Error", "Database failed to respond when adding information. Event was: " + str(self.event[0]))
            if str(self.event[0]).isnumeric() is False:
                print("Home ID non numeric")
                self.event[0] = 999
            if str(self.event[2]).isnumeric() is False:
                print("Subject ID non numeric")
                self.event[2] = 4649038020852
            if str(self.event[1]).isnumeric() is False:
                print("Regular ID non numeric")
                self.event[1] = 4649038020852
            self.event[3] = "ERROR"
            self.event[4] = "ERROR"
            self.eventToDatabase(attempt + 1)
            return False


    # Code used for commiting failed sales orders
    def pushFailedOrder(self):

        # Get the sales order from the sales event stored when the object was initiallized.
        result = 0
        orderGet = self.getSalesOrder()

        # Attempt to post the sales order
        orderPost = self.postSalesOrder()

        # If orderPost or orderGet have failed, set the pushed state to 0. Else, its 1
        if not orderPost or not orderGet:
            result = 0

        if (self.retry == 1 and self.postState2) or (self.retry == 2 and self.postState1) or (self.retry == 3 and self.postState1):
            result = 1

        # Add 1 to the attempts there has been to post the order, set that as the new attempts and set the pushed state
        # to te result of the checks above
        attempt = self.event[7] + 1
        SalesOrderDAO.setShopifyOrderAttemptsById(self.event[1], attempt)

        if self.retry == 1:
            SalesOrderDAO.setShopifyAccountancySuccessById(self.event[1], result)
        else:
            SalesOrderDAO.setShopifyOrderSuccessById(self.event[1], result)


    # Fire through the process for a order from shopify.
    def commitAll(self):

        if self.debug:
            SalesOrderDAO.setLogsToDatabase("[SO][DEBUG]SalesOrderProcessing",
                                               "Processing new sales order. Event is " + str(
                                                           self.event[0]))

        if not self.getSalesOrder():
            SalesOrderDAO.setLogsToDatabase("[SO][ERROR]GettingShopifyOrderFromEvent",
                                               "Higher up error pointer for getting sales order from event. Event is " + str(
                                                           self.event[0]))
            return False

        # Record 5 is the pushed field in db, while record 8 is the accountancy field. If record 5 is 1,
        # then the order has been pushed to buisness central.
        # If record 8 is 1, then the order has been pushed to accountancy. If record 5 is 0,
        # then the order has not been pushed to buisness central.
        # If record 8 is 0, then the order has not been pushed to accountancy.

        self.postSalesOrder()

        self.event[5] = int(self.postState1)
        self.event[8] = int(self.postState2)
        if self.accountancy:

            # If the process was WAL Accountancy, then check both post states.
            # If one is false, then an issue has occured.

            if not self.postState1 or not self.postState2:
                SalesOrderDAO.setLogsToDatabase("[SO][ERROR]OrderNotPushed",
                                                       "Order(s) has failed to push, setting to 0. Event was " + str(
                                                                   self.event[0]) + " with accountancy of " + str(self.accountancy)
                                                + " with post states of " + str(self.postState1) +
                                                       " " + str(self.postState2))

        # If the process was not WAL Accountancy, then check only the first post state.
        else:
            if not self.postState1:
                SalesOrderDAO.setLogsToDatabase("[SO][ERROR]OrderNotPushed",
                                                       "Order(s) has failed to push, setting to 0. Event was " + str(
                                                                   self.event[0]) + " with accountancy of " + str(self.accountancy)
                                                + " with post states of " + str(self.postState1) +
                                                       " " + str(self.postState2))

        if self.retry == 0:
            dbOrderPost = self.eventToDatabase()

            if dbOrderPost:
                return True
            else:
                return False

        else:
            if self.postState1 and self.postState2:
                return True
            else:
                return False

    def getEvent(self):

        return self.event

    def getReason1(self):

        return self.reason1

    def getReason2(self):

        return self.reason2

    def setRetry(self, retry):

        self.retry = retry
