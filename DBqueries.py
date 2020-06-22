# This file will be used as an import for __init__.py containing all of the SQL queries
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="frugally",
    password="Shoelas",
    database="Frugally"
)
cursor = conn.cursor()

def getSQLNordstrom():

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

def getSQLNike():

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



if __name__ == '__main__':
    getSQLNordstrom()
    getSQLNike()
