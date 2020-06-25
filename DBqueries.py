# This file will be used as an import for __init__.py containing all of the SQL queries
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="frugally",
    password="Shoelas",
    database="Frugally"
)
cursor = conn.cursor()

# The goal of this function is to return a set of products
# whose attributes match that of the filters
# and are sorted in order of highest discount to lowest
def getSQLdiscount(filters):

    # Parse out the filters
    if(filters!=None):
        gender = str(filters[0][1]).lower()
        filtervendor = filters[1][1]
        filterbrands = filters[2][1]
    else:
        gender = "all"
        filtervendor = "all"
        filterbrands = "all"

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM NordstromRackMen WHERE', gender)

    item = cursor.fetchall()


# The goal of this function is to return a set of products
# whose attributes match that of the filters
# and are sorted in order of price, depending on the boolean value of highlow
def getSQLprice(filters, highlow):
    pass


#This function simply fetches all nordstromrack content
def getSQLNordstrom():

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM NordstromRackMen')

    item = cursor.fetchall()

    cursor.execute('SELECT * FROM NordstromRackWomen')

    item2 = cursor.fetchall()
    item = item + item2
    #for i in item:
    #    print(i)

    cursor.close()
    return item


#This funciton simply fetches all nike content
def getSQLNike():

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM NikeMen')

    item = cursor.fetchall()

    cursor.execute('SELECT * FROM NikeWomen')

    item2 = cursor.fetchall()
    item = item + item2
    #for i in item:
    #    print(i)

    cursor.close()
    return item

