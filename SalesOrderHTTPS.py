import requests
import json
import time
from Constants import Constants
import re
import SalesOrderDAO

bcKeys = Constants.BC_KEY
secBcKeys = Constants.SECONDARY_BC_KEY
# Constructs a component for the HTTP request
def constructHTTPComponent(type, pairs):
    returnDict = {}

    for pair in pairs:
        returnDict[pair[0]] = pair[1]

    # If type is B, return a json object as this is the body of the request
    if type == "B":
        return json.dumps(returnDict)

    # Else this is likely a header, return a dictionary
    else:
        return returnDict

# Returns the data given from a request given to BC
def bcGetRequest(url, type="D"):
    headers = constructHTTPComponent("H", [["Authorization", bcKeys], ["Content-Type", "application/json"]])
    try:
        response = requests.request("GET", url, headers=headers)

    except Exception as e:
        SalesOrderDAO.setLogsToDatabase("[SO][ERROR]BCGetRequest",
                                        "Faliure to get a response with URL " + url + " and error " + str(e))
        return None

    return response

# Send a patch request to refresh a webhook subscription
def bcPatchRequest(sub, notUrl, clientState):
    url = "REDACTED('" + sub + "')"

    payload = constructHTTPComponent("B", [["notificationUrl", notUrl], ["resource",
                                                                              "REDACTED"],
                                                ["clientState", clientState]])
    headers = constructHTTPComponent("H", [["Authorization", bcKeys], ["Content-Type", 'application/json'],
                                                ["If-Match", "*"]])
    response = requests.patch(url, headers=headers, data=payload)

    return response

## Send a post request to create a new webhook
def bcHookPost(notUrl, clientState):
    url = "REDACTED"

    payload = constructHTTPComponent("B", [["notificationUrl", notUrl], ["resource",
                                                                              "REDACTED"],
                                                ["clientState", clientState]])
    headers = constructHTTPComponent("H", [["Authorization", bcKeys], ["Content-Type", 'application/json']])
    response = requests.post(url, headers=headers, data=payload)

    return response

# Send a post request to send off the sales order
def bcPostRequestSO(salesOrderLines, bulkPayload, accounts=[], company=None,
                        version="1.1", test=False):  # creates and sends the payload to bc

    # Logic handling the different variables which could constitute of the target url for request.
    # Note that later on there may be a need to locate different accounts.
    if not test:
        if company is not None:
            if company == "WAL":

                # Company code was got via email
                # REDACTED
                # Use the live api to get accounts connected to live.
                company = Constants.WAL_ID

            else:
                company = Constants.CPC_ID
            target = "REDACTED" + version + "REDACTED" + \
                     str(company) + "REDACTED" + "REDACTED"
        else:

            # If company is not wear a label, the api defaults to childsplay's default.
            target = "REDACTED" + version + "REDACTED"
    else:
        target = "REDACTED"

    # FORMAT IS [Item, quant, price] or [Account, quantity, price]
    completedSaleLines = []


    # If the sales order version is not 1.0, then behave like normal, if it is 1.0, then dont bother using a price as 1.0 doesnt use a price
    if version != "1.0":
        for i in salesOrderLines:
            completedSaleLines.append(constructHTTPComponent("L", [["itemId", i[0]], ["quantity", i[1]], ["unitPrice", i[2]]]))

    else:
        for i in salesOrderLines:
            completedSaleLines.append(constructHTTPComponent("L", [["itemId", i[0]], ["quantity", i[1]]]))

    for j in accounts:
        completedSaleLines.append(constructHTTPComponent("L", [["accountId", j[0]], ["quantity", j[1]], ["unitPrice", j[2]]]))


    # FORMAT IS [customerNo, PON, reqDelDate, shipName, shipAd1, shipAd2, shipCit, shipCounty, shipPost, shipCountry]
    body = constructHTTPComponent("B", [["customerNumber", bulkPayload[0]], ["purchaseOrderNo", bulkPayload[1]],
                                             ["requiredDeliveryDate", bulkPayload[2]], ["shippingName", bulkPayload[3]],
                                             ["shippingAddress", bulkPayload[4]], ["shippingAddress2", bulkPayload[5]],
                                             ["shippingCity", bulkPayload[6]], ["shippingCounty", bulkPayload[7]],
                                             ["shippingPostcode", bulkPayload[8]], ["shippingCountry", bulkPayload[9]],
                                             ["salesOrderLines", completedSaleLines]])

    headers = constructHTTPComponent("H", [["Authorization", Constants.SECONDARY_BC_KEY], ["Content-Type", "application/json"]])

    try:
        response = requests.request("POST", target, headers=headers, data=body)

    except Exception as e:
        SalesOrderDAO.setLogsToDatabase("[SO][ERROR]BCPostRequest",
                                           "Exception occured with original request. Order was" + str(
                                                       bulkPayload[1]) + " with error of: " + str(e))
        return False, 1

    print(response, " was sales order post response with json of ", response.json())

    if len(re.findall("locked", str(response.json()))) != 0:
        SalesOrderDAO.setLogsToDatabase("[SO][ERROR]BCPostRequest",
                                           "BC has locked tables. Sales order therefore failed. Order was " + str(
                                                       bulkPayload[1]) + " with response of " + str(response.json()))
        return False, 3

    if len(re.findall("error", str(response.json()))) != 0:
        SalesOrderDAO.setLogsToDatabase("[SO][ERROR]BCPostRequest",
                                           "Error returned from BC, assuming no sales order was actually posted. Order was " + str(
                                                       bulkPayload[1]) + " with response of " + str(response.json()))
        return False, 4

    if response.status_code != 200 and response.status_code != 201:
        SalesOrderDAO.setLogsToDatabase("[SO][ERROR]BCPostRequest",
                                           "Faliure to trigger requests code. Order failed was " + str(
                                                       bulkPayload[1]) + " with error of: " + str(response.json()))
        return False, 5

    return True, 0


def urlFilterByCpCodeSKU(url, sku):

    return url + "REDACTED" + sku + "'"

def urlFilterByMasterCpCodeSKU(url, msku):

    return url + "REDACTED" + msku + "'"


class ShopifyApiHelper:

    # TODO: MAKE THIS INTO A TRUE SINGLETON

    def __init__(self):

        self.shopifyUrl = Constants.WAL_URL
        self.bcKeys = Constants.BC_KEY
        self.lastShopifyUse = time.time()
        self.debug = True

    def apiRestrictor(self):

        while time.time() - self.lastShopifyUse < 0.5:
            time.sleep(0.1)
        self.lastShopifyUse = time.time()

    ## SHOPIFY API TOOLS ##

    def constructShopifyGetRequest(self, target, filterList=None, apiKey=""):

        self.apiRestrictor()

        if filterList is None:
            filterList = []

        localShopifyUrl = self.shopifyUrl

        def constructFilterList(filterList):

            if not filterList:
                return ""

            resultString = "?" + str(filterList[0][0]) + "=" + str(filterList[0][1])
            filterList.pop(0)

            for item in filterList:
                resultString = resultString + "&" + item[0] + "=" + item[1]

            return resultString


        finalUrl = localShopifyUrl + target + constructFilterList(filterList)
        response = requests.get(finalUrl)
        return response


    def constructShopifyPostRequest(self, target, headers={}, body=json.dumps({}), apiKey="Default"):

        self.apiRestrictor()

        localShopifyUrl = self.shopifyUrl

        if headers is None:
            headers = {}
        url = localShopifyUrl + target

        response = requests.post(url, headers=headers, data=body)
        return response