import datetime
import SalesOrderDBCore as DBCon

## TODO: MERGE THIS WITH THE DBCon File

def getEventIdOrSetEventIDIfExists(event):

    # I initally built this function with recursion - unfortunatley, this caused too many bugs.
    # Now, a check takes place if the ID exists. if the check returns nothing, the new event
    # is built and its id is got.

    ID = DBCon.DBConnection.execute_query("SELECT event_id FROM event_type WHERE event_type = %s", event)
    if not ID:
        DBCon.DBConnection.execute_query("INSERT INTO event_type (event_type) VALUES (%s)", event)
        ID = DBCon.DBConnection.execute_query("SELECT event_id FROM event_type WHERE event_type = %s", event)

    return ID[0] # Database doing database things and returning arrays

def setLogsToDatabase(eventName, content):

    # Check which table is passed in as a parameter, push the event to the database.

    DBCon.DBConnection.execute_query("INSERT INTO event_logs (event_id, time, content) VALUES (%s, %s, %s)",
                         [getEventIdOrSetEventIDIfExists(eventName), str(datetime.datetime.now()), content], False)


def updateLatestShopifyItem(previousid, id):

    DBCon.DBConnection.execute_query("UPDATE shopifyorders SET last_item = 0 WHERE subject_id = %s", [previousid])
    DBCon.DBConnection.execute_query("UPDATE shopifyorders SET last_item = 1 WHERE subject_id = %s", [id])

def setAllShopifyOrders(manylist):

    sql = "INSERT INTO shopifyorders (home_number, id, subject_id, created_at, message, pushed, last_item, attempts, accountancy_push) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    DBCon.DBConnection.execute_query(sql, manylist, False, True)

def setOneShopifyOrder(order):

    sql = "INSERT INTO shopifyorders (home_number, id, subject_id, created_at, message, pushed, last_item, attempts, accountancy_push) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    DBCon.DBConnection.execute_query(sql, order)

def setShopifyOrderAttemptsById(id, val):

    sql = "UPDATE shopifyorders SET attempts = %s WHERE id = %s"
    DBCon.DBConnection.execute_query(sql, [val, id])

def setShopifyOrderSuccessById(id, val):

    sql = "UPDATE shopifyorders SET pushed = %s WHERE id = %s"
    DBCon.DBConnection.execute_query(sql, [val, id])

def getAllShopifyItemFaliures():

    sql = "SELECT * FROM shopifyorders WHERE pushed = 0"
    return DBCon.DBConnection.execute_query(sql, None, True)

def deleteShopifyRecord(id):

    sql = "DELETE FROM shopifyorders WHERE id = %s"
    DBCon.DBConnection.execute_query(sql, [id])

# Does what it says on the tin.
def getLatestShopifyItem():

    sql = "SELECT * FROM shopifyorders WHERE last_item = 1"
    return DBCon.DBConnection.execute_query(sql, None)

def logTableTruncater():

    sql = "TRUNCATE TABLE event_logs"
    DBCon.DBConnection.execute_query(sql, None, False)

def setShopifyAccountancySuccessById(id, val):

    sql = "UPDATE shopifyorders SET accountancy_push = %s WHERE id = %s"
    DBCon.DBConnection.execute_query(sql, [val, id])

def getUnitCostWithSku(sku):

    return DBCon.DBConnection.execute_query("SELECT unit_cost FROM sku_unit_cost WHERE sku = %s", [sku])

def getAllShopifyAccountancyFaliures():

    sql = "SELECT * FROM shopifyorders WHERE accountancy_push = 0"
    return DBCon.DBConnection.execute_query(sql, None, True)