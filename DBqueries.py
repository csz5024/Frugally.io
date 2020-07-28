# This file will be used as an import for __init__.py containing all of the SQL queries
import mysql.connector
import sys
import re
import json
import urllib.request

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
def getSQLdiscount_steve(filters):

    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
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
        if(filtervendor == 'all'):
            sql = "SELECT * FROM NordstromRackMen as N UNION ALL SELECT * FROM NikeMen as M ORDER BY discount DESC;"
            #vars = (gender)
            cursor.execute(sql)
            item = cursor.fetchall()
        if(filterbrands!="all" and ("Nike" not in filterbrands)):
            temp = ""
            for i in filterbrands:
                temp += "brand='%s' OR " % i
            temp = temp.strip("OR ")
            sql = "SELECT * FROM NordstromRackMen WHERE "+temp+"ORDER BY discount DESC"
            cursor.execute(sql)
            item = cursor.fetchall()
        else:
        #filters vendor  (only accounts for Nike and Nordstrom Rack right now)
            if(filtervendor=='NordstromRack'):
                sql = "SELECT * FROM NordstromRackMen ORDER BY discount DESC;"
                cursor.execute(sql)
                item = cursor.fetchall()


        if(filterbrands!="all" and ("Nike" not in filterbrands)):
            temp = ""
            for i in filterbrands:
                temp += "brand='%s' OR " % i
            temp = temp.strip("OR ")
            sql = "SELECT * FROM NordstromRackMen WHERE "+temp+"ORDER BY discount DESC"
            cursor.execute(sql)
            item = cursor.fetchall()
        else:
            sql ="SELECT * FROM NikeMen ORDER BY discount DESC;"
            cursor.execute(sql)
            item = cursor.fetchall()
        if(filterbrands!="all"):
            temp = ""
            for i in filterbrands:
                temp += "brand='%s' OR " % i
            temp = temp.strip("OR ")
            sql = "SELECT * FROM NikeMen WHERE "+temp+"ORDER BY discount DESC"
            cursor.execute(sql)
            item = cursor.fetchall()

        else:
            if(filtervendor=='all'):
                sql = "SELECT * FROM NordstromRackWomen as N UNION ALL SELECT * FROM NikeWomen as M ORDER BY discount DESC;"
                #vars = (gender)
                cursor.execute(sql)
                item = cursor.fetchall()
                if(filterbrands!="all" and ("Nike" not in filterbrands)):
                    temp = ""
                    for i in filterbrands:
                        temp += "brand='%s' OR " % i
                    temp = temp.strip("OR ")
                    sql = "SELECT * FROM NordstromRackWomen WHERE "+temp+"ORDER BY discount DESC"
                    cursor.execute(sql)
                    item = cursor.fetchall()

    else:
        #filters vendor (only accounts for Nike and Nordstrom Rack right now)
        if(filtervendor=='NordstromRack'):
            sql = "SELECT * FROM NordstromRackWomen ORDER BY discount DESC;"
            cursor.execute(sql)
            item = cursor.fetchall()
            if(filterbrands!="all" and ("Nike" not in filterbrands)):
                temp = ""
                for i in filterbrands:
                    temp += "brand='%s' OR " % i
                temp = temp.strip("OR ")
                sql = "SELECT * FROM NordstromRackWomen WHERE "+temp+"ORDER BY discount DESC"
                cursor.execute(sql)
                item = cursor.fetchall()

        else:
            sql ="SELECT * FROM NikeWomen ORDER BY discount DESC;"
            cursor.execute(sql)
            item = cursor.fetchall()
            if(filterbrands!="all"):
                temp = ""
                for i in filterbrands:
                    temp += "brand='%s' OR " % i
                temp = temp.strip("OR ")
                sql = "SELECT * FROM NordstromRackWomen WHERE "+temp+"ORDER BY discount DESC"
                cursor.execute(sql)
                item = item + cursor.fetchall()


    cursor.close()
    conn.close()
    return item



def getSQLdiscount(filters):
    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
        database="Frugally"
    )
    cursor = conn.cursor()

    errorlogger="filters"

    # Parse out the filters
    if(filters!=None):
        gender = str(filters[0][1]).lower()
        filtervendor = filters[1][1]
        filterbrands = filters[2][1]
        filterrange = filters[3][1]

        try:
            prange = "WHERE ("
            for i in filterrange:
                i = i.split("-")
                i[0] = i[0].strip("$")
                i[1] = i[1].strip("$")
                prange += "price>=%.2f AND price<=%.2f OR " % (float(i[0]), float(i[1]))
            prange = prange.strip("OR ")
            prange += ")"
        except:
            prange = ""

        if(len(filterbrands)>=1):
            if(len(prange)>1):
                temp = "AND("
            else:
                temp = "WHERE ("
            for i in filterbrands:
                temp += "brand='%s' OR " % i
            temp = temp.strip("OR ")
            temp += ")"
        else:
            temp = ""

    else:
        filtervendor = "all"
        temp = ""
        prange = ""

    #errorlogger = "gender: %s, filtervendor:%s, prange:%s, temp:%s" % (gender, filtervendor, prange, temp)

    if(gender == 'men'):
        if(filterbrands!="all" and ("Nike" not in filterbrands)):
            sql = "SELECT * FROM NordstromRackMen "+prange+temp+" ORDER BY discount DESC"
            #errorlogger = sql
        elif(filterbrands!="all"):
            if(len(filtervendor)==1 and filtervendor[0] == "Nike"):
                sql = "SELECT * FROM NikeMen "+prange+temp+" ORDER BY discount DESC"
            elif(len(filtervendor)==1 and filtervendor != "all"):
                sql = "SELECT * FROM NordstromRackMen "+prange+temp+" ORDER BY discount DESC"
            else:
                sql = "SELECT * FROM NordstromRackMen "+prange+temp+" UNION ALL SELECT * FROM NikeMen "+prange+" ORDER BY discount DESC"
            #errorlogger = sql
        else:
            if(len(filtervendor)==1 and filtervendor[0] == "Nike"):
                sql = "SELECT * FROM NikeMen "+prange+" ORDER BY discount DESC"
            elif(len(filtervendor)==1 and filtervendor != "all"):
                sql = "SELECT * FROM NordstromRackMen "+prange+" ORDER BY discount DESC"
            else:
                sql = "SELECT * FROM NordstromRackMen "+prange+" UNION ALL SELECT * FROM NikeMen "+prange+" ORDER BY discount DESC"

    # Women
    else:
        if(filterbrands!="all" and ("Nike" not in filterbrands)):
            sql = "SELECT * FROM NordstromRackWomen "+prange+temp+" ORDER BY discount DESC"
        elif(filterbrands!="all"):
            if(len(filtervendor)==1 and filtervendor[0] == "Nike"):
                sql = "SELECT * FROM NikeWomen "+prange+temp+" ORDER BY discount DESC"
            elif(len(filtervendor)==1 and filtervendor != "all"):
                sql = "SELECT * FROM NordstromRackWomen "+prange+temp+" ORDER BY discount DESC"
            else:
                sql = "SELECT * FROM NordstromRackWomen "+prange+temp+" UNION ALL SELECT * FROM NikeWomen "+prange+" ORDER BY discount DESC"
        else:
            if(len(filtervendor)==1 and filtervendor[0] == "Nike"):
                sql = "SELECT * FROM NikeWomen "+prange+" ORDER BY discount DESC"
            elif(len(filtervendor)==1 and filtervendor != "all"):
                sql = "SELECT * FROM NordstromRackWomen "+prange+" ORDER BY discount DESC"
            else:
                sql = "SELECT * FROM NordstromRackWomen "+prange+"UNION ALL SELECT * FROM NikeWomen "+prange+" ORDER BY discount DESC" 

    cursor.execute(sql)
    item = cursor.fetchall()


    cursor.close()
    conn.close()
    return item, errorlogger


# The goal of this function is to return a set of products
# whose attributes match that of the filters
# and are sorted in order of price, depending on the boolean value of highlow
def getSQLprice(filters, highlow):
    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
        database="Frugally"
    )
    cursor = conn.cursor()

    errorlogger = ""

    # Parse out the filters
    if(filters!=None):
        gender = str(filters[0][1]).lower()
        filtervendor = filters[1][1]
        filterbrands = filters[2][1]
        filterrange = filters[3][1]

        try:
            prange = "WHERE ("
            for i in filterrange:
                i = i.split("-")
                i[0] = i[0].strip("$")
                i[1] = i[1].strip("$")
                prange += "price>=%.2f AND price<=%.2f OR " % (float(i[0]), float(i[1]))
            prange = prange.strip("OR ")
            prange += ")"
        except:
            prange = ""

        if(len(filterbrands)>=1):
            if(len(prange)>1):
                temp = "AND("
            else:
                temp = "WHERE ("
            for i in filterbrands:
                temp += "brand='%s' OR " % i
            temp = temp.strip("OR ")
            temp += ")"
        else:
            temp = ""

        if(len(filtervendor)==0):
            filtervendor="all"
    else:
        filtervendor="all"
        prange=""
        temp=""


    if(gender == 'men'):
        if(filterbrands!="all" and ("Nike" not in filterbrands)):
            sql = "SELECT * FROM NordstromRackMen "+prange+temp+" ORDER BY price"
        elif(filterbrands!="all"):
            if(len(filtervendor)==1 and filtervendor[0] == "Nike"):
                sql = "SELECT * FROM NikeMen "+prange+temp+" ORDER BY price"
            elif(len(filtervendor)==1 and filtervendor != "all"):
                sql = "SELECT * FROM NordstromRackMen "+prange+temp+" ORDER BY price"
            else:
                sql = "SELECT * FROM NordstromRackMen "+prange+temp+" UNION ALL SELECT * FROM NikeMen "+prange+" ORDER BY price"
        else:
            if(len(filtervendor)==1 and filtervendor[0] == "Nike"):
                sql = "SELECT * FROM NikeMen "+prange+" ORDER BY price"
            elif(len(filtervendor)==1 and filtervendor != "all"):
                sql = "SELECT * FROM NordstromRackMen "+prange+" ORDER BY price"
            else:
                sql = "SELECT * FROM NordstromRackMen "+prange+" UNION ALL SELECT * FROM NikeMen "+prange+" ORDER BY price"

    # Women
    else:
        if(filterbrands!="all" and ("Nike" not in filterbrands)):
            sql = "SELECT * FROM NordstromRackWomen "+prange+temp+" ORDER BY price"
        elif(filterbrands!="all"):
            if(len(filtervendor)==1 and filtervendor[0] == "Nike"):
                sql = "SELECT * FROM NikeWomen "+prange+temp+" ORDER BY price"
            elif(len(filtervendor)==1 and filtervendor != "all"):
                sql = "SELECT * FROM NordstromRackWomen "+prange+temp+" ORDER BY price"
            else:
                sql = "SELECT * FROM NordstromRackWomen "+prange+temp+" UNION ALL SELECT * FROM NikeWomen "+prange+" ORDER BY price"
        else:
            if(len(filtervendor)==1 and filtervendor[0] == "Nike"):
                sql = "SELECT * FROM NikeWomen "+prange+" ORDER BY price"
            elif(len(filtervendor)==1 and filtervendor != "all"):
                sql = "SELECT * FROM NordstromRackWomen "+prange+" ORDER BY price"
            else:
                sql = "SELECT * FROM NordstromRackWomen "+prange+" UNION ALL SELECT * FROM NikeWomen "+prange+" ORDER BY price"

    if(highlow):
        sql = sql+" DESC"
    cursor.execute(sql)
    item = cursor.fetchall()

    cursor.close()
    conn.close()
    return item, errorlogger

#these are used for the filtermenu
def getMaxPriceMen():
    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
        database="Frugally"
    )
    cursor = conn.cursor()

    sql = "SELECT MAX(price) FROM (SELECT * FROM NordstromRackMen as N UNION ALL SELECT * FROM NikeMen as M) as F;"
    cursor.execute(sql)
    item = cursor.fetchall()
    cursor.close()
    conn.close()
    return item[0][0]

def getMaxPriceWomen():
    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
        database="Frugally"
    )
    cursor = conn.cursor()

    sql = "SELECT MAX(price) FROM (SELECT * FROM NordstromRackWomen as N UNION ALL SELECT * FROM NikeWomen as M) as F;"
    cursor.execute(sql)
    item = cursor.fetchall()
    cursor.close()
    conn.close()
    return item[0][0]


#This function simply fetches all nordstromrack content
def getSQLNordstrom():

    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
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
        password="Shoelas20",
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


# Used to search Frugally DB for product info by product link
# Used exclusively to update the product history table
def findByLink(link):
    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
        database="Frugally"
    )
    cursor = conn.cursor()

    sql = "SELECT EXISTS(SELECT * FROM(SELECT * FROM NordstromRackMen as N UNION ALL SELECT * FROM NikeMen as M) as X WHERE link=%s)"
    sql2 = "SELECT EXISTS(SELECT * FROM(SELECT * FROM NordstromRackWomen as N UNION ALL SELECT * FROM NikeWomen as M) as X WHERE link=%s)"
    vals = (str(link),)
    cursor.execute(sql, vals)
    item = cursor.fetchall()
    cursor.execute(sql2, vals)
    item2 = cursor.fetchall()

    if(item[0][0]!=0):
        sql = "SELECT * FROM(SELECT * FROM NordstromRackMen as N UNION ALL SELECT * FROM NikeMen as M) as X WHERE link=%s"
        vals = (str(link),)
        cursor.execute(sql, vals)
        item = cursor.fetchall()
    elif(item2[0][0]!=0):
        sql = "SELECT * FROM(SELECT * FROM NordstromRackWomen as N UNION ALL SELECT * FROM NikeWomen as M) as X WHERE link=%s"
        vals = (str(link),)
        cursor.execute(sql, vals)
        item = cursor.fetchall()
    else:
        return "Big problem, not found in databases"
    return item



# gathers data on user once product link is clicked
'''
Data Gathered:

Product History - An all-time list of products clicked, identified by link
Links Clicked - Who clicked what and how many times for each product
Users - A list of Users identified by IP address who clicked on at least 1 product
'''
def Collect(link, userid):
    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
        database="BigDataDave"
    )
    cursor = conn.cursor()

    #this gets geographic information on the IP address
    url = "https://freegeoip.app/json/"+str(userid)
    with urllib.request.urlopen(url) as response:
        data = json.load(response)

    ip=data['ip']
    country=data['country_name']
    region=data['region_name']
    city=data['city']
    zipcode=data['zip_code']
    timezone=data['time_zone']

    errorval = "Error on link %s: " % link

    try:
        #updates the Users Table
        sql = "SELECT EXISTS(SELECT * FROM Users WHERE addr=%s)"
        vals = (str(ip),)
        cursor.execute(sql, vals)
        item = cursor.fetchall()
        if(item[0][0]!=0):
            sql = "UPDATE Users SET linksclicked=linksclicked+1 WHERE addr=%s"
            vals = (str(ip),)
            cursor.execute(sql, vals)
        else:
            sql = "INSERT INTO Users(addr, city, state, country, zipcode, timezone, linksclicked) VALUES(%s, %s, %s, %s, %s, %s, %s);"
            vals = (ip, city, region, country, zipcode, timezone, 1,)
            cursor.execute(sql, vals)

        #updates the product history table
        sql = "SELECT EXISTS(SELECT * FROM ProductHistory WHERE link=%s)"
        vals = (str(link),)
        cursor.execute(sql, vals)
        item = cursor.fetchall()
        if(item[0][0]==0):
            items = findByLink(link)
            #return errorval + str(items)
            sql = "INSERT INTO ProductHistory(vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            vals = (items[0][0], items[0][1], items[0][2], items[0][3], items[0][4], items[0][5], items[0][6], items[0][7], items[0][8],)
            cursor.execute(sql, vals)

        #updates the links clicked table
        sql = "SELECT EXISTS(SELECT * FROM LinksClicked WHERE addr=%s AND link=%s)"
        vals = (str(ip), str(link),)
        cursor.execute(sql, vals)
        item = cursor.fetchall()
        if(item[0][0]!=0):
            sql = "UPDATE LinksClicked SET clicked=clicked+1 WHERE link='%s' and addr='%s'" % (str(link), str(ip))
            cursor.execute(sql)
        else:
            sql = "INSERT INTO LinksClicked(link, addr, clicked) VALUES(%s, %s, %s)"
            vals = (str(link), str(ip), 1,)
            cursor.execute(sql, vals)

        cursor.close()
        conn.commit()
        conn.close()
        return "Success"
    except:
        cursor.close()
        conn.close()
        return "FAILED"
