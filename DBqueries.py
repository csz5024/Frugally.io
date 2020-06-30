# This file will be used as an import for __init__.py containing all of the SQL queries
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="frugally",
    password="Shoelas",
    database="Frugally"
)
cursor = conn.cursor()

# Root of the filters tree
# Makes a nested function call
def getSQLsort(filters, gender):

    sortmethod = filters.pop(0)
    sortmethod = sortmethod[1]
    filters.insert(0,['gender', str(gender)])

    if(sortmethod == 'discount'):
        objects = getSQLdiscount(filters)
    elif(sortmethod == 'low'):
        objects = getSQLprice(filters, highlow=False)
    else:
        objects = getSQLprice(filters, highlow=True)

    return objects


# The goal of this function is to return a set of products
# whose attributes match that of the filters
# and are sorted in order of highest discount to lowest
def getSQLdiscount(filters):

    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas",
        database="Frugally"
    )

    # Parse out the filters
    if(filters!=None):
        gender = str(filters[0][1]).lower()
        filtervendor = filters[1][1]
        filterbrands = filters[2][1]
    else:
        gender = "all"
        filtervendor = "all"
        filterbrands = "all"

    #only filters gender and sorts by discount
    cursor = conn.cursor()

    if(gender=='men'):

        sql = "SELECT * FROM NordstromRackMen as N UNION ALL SELECT * FROM NikeMen as M ORDER BY discount DESC;"
        #vars = (gender)
        cursor.execute(sql)
        item = cursor.fetchall()

    else:

        sql = "SELECT * FROM NordstromRackWomen as N UNION ALL SELECT * FROM NikeWomen as M ORDER BY discount DESC;"
        #vars = (gender)
        cursor.execute(sql)
        item = cursor.fetchall()

    cursor.close()
    conn.close()
    return item


# The goal of this function is to return a set of products
# whose attributes match that of the filters
# and are sorted in order of price, depending on the boolean value of highlow
def getSQLprice(filters, highlow):
    pass


#This function simply fetches all nordstromrack content
def getSQLNordstrom():

    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas",
        database="Frugally"
    )
    cursor = conn.cursor()


    cursor = conn.cursor()
    cursor.execute('SELECT * FROM NordstromRackMen')

    item = cursor.fetchall()

    cursor.execute('SELECT * FROM NordstromRackWomen')

    item2 = cursor.fetchall()
    item = item + item2
    #for i in item:
    #    print(i)

    cursor.close()
    conn.close()
    return item


#This funciton simply fetches all nike content
def getSQLNike():

    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas",
        database="Frugally"
    )
    cursor = conn.cursor()


    cursor = conn.cursor()
    cursor.execute('SELECT * FROM NikeMen')

    item = cursor.fetchall()

    cursor.execute('SELECT * FROM NikeWomen')

    item2 = cursor.fetchall()
    item = item + item2
    #for i in item:
    #    print(i)

    cursor.close()
    conn.close()
    return item

