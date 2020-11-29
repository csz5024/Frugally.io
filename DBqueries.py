
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

def deleteSoldOut(item):
    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
        database="Frugally"
    )
    cursor = conn.cursor()

    if(item[0][1] == "Nike"):
        if(item[0][2] == "Women"):
            sql = "DELETE FROM NikeWomen WHERE PID=%s" % item[0][0]
        else:
            sql = "DELETE FROM NikeMen WHERE PID=%s" % item[0][0]
    elif(item[0][1] == "Nordstrom Rack"):
        if(item[0][2] == "Women"):
            sql = "DELETE FROM NordstromRackWomen WHERE PID=%s" % item[0][0]
        else:
            sql = "DELETE FROM NordstromRackMen WHERE PID=%s" % item[0][0]
    else:
        return "Big problem not found"

    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    return "Success"


# Used to search Frugally DB for product info by product link
# Used exclusively to update the product history table
def findByPID(pid):
    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
        database="Frugally"
    )
    cursor = conn.cursor()

    sql = "SELECT EXISTS(SELECT * FROM(SELECT * FROM NordstromRackMen as N UNION ALL SELECT * FROM NikeMen as M) as X WHERE PID=%s)"
    sql2 = "SELECT EXISTS(SELECT * FROM(SELECT * FROM NordstromRackWomen as N UNION ALL SELECT * FROM NikeWomen as M) as X WHERE PID=%s)"
    vals = (pid,)
    #return vals
    cursor.execute(sql, vals)
    item = cursor.fetchall()
    cursor.execute(sql2, vals)
    item2 = cursor.fetchall()

    if(item[0][0]!=0):
        sql = "SELECT * FROM(SELECT * FROM NordstromRackMen as N UNION ALL SELECT * FROM NikeMen as M) as X WHERE PID=%s"
        vals = (pid,)
        cursor.execute(sql, vals)
        item = cursor.fetchall()
    elif(item2[0][0]!=0):
        sql = "SELECT * FROM(SELECT * FROM NordstromRackWomen as N UNION ALL SELECT * FROM NikeWomen as M) as X WHERE PID=%s"
        vals = (pid,)
        cursor.execute(sql, vals)
        item = cursor.fetchall()
    else:
        return "Big problem, not found in databases"
    cursor.close()
    conn.close()
    return item



# gathers data on user once product link is clicked
'''
Data Gathered:

Product History - An all-time list of products clicked, identified by link
Links Clicked - Who clicked what and how many times for each product
Users - A list of Users identified by IP address who clicked on at least 1 product
'''
def Collect(clickeditem, userid):
    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
        database="BigDataDave"
    )
    cursor = conn.cursor()


    #this gets geographic information on the IP address
    url = "https://ipinfo.io/"+str(userid)+"/json"
    with urllib.request.urlopen(url) as response:
        data = json.load(response)

    #return data
    ip=data['ip']
    if(ip == '192.168.1.1'):
        return "Success"
    country=data['country']
    region=data['region']
    city=data['city']
    zipcode=data['postal']
    timezone=data['timezone']
    if('org' in data):
        org = data['org']
    else:
        org = None
    if('hostname' in data):
        hostname = data['hostname']
        hostname = hostname.split(".")
    else:
        hostname = ["No Hostname"]

    errorval = "Error on item %s: " % clickeditem[0][9]
# if "googlebot" in hostname: end function  else:continue
    if "googlebot" in hostname:
        return "Google Bot"
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
            sql = "INSERT INTO Users(addr, city, state, country, zipcode, timezone, linksclicked, org) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
            vals = (ip, city, region, country, zipcode, timezone, 1, org,)
            cursor.execute(sql, vals)

        #updates the product history table
        sql = "SELECT EXISTS(SELECT * FROM ProductHistory WHERE link='%s')" % clickeditem[0][9]
        cursor.execute(sql)
        item = cursor.fetchall()
        #if the product is not found in the table
        if(item[0][0]==0):
            maxpid = "SELECT MAX(PID) FROM ProductHistory"
            cursor.execute(maxpid)
            maxpid = cursor.fetchall()
            if(maxpid[0][0] != None):
                maxpid = maxpid[0][0] + 1
            else:
                maxpid = 0
            sql = "INSERT INTO ProductHistory(PID, vendor, gender, title, brand, retailprice, price, discount, imagelink, link) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            vals = (maxpid, clickeditem[0][1], clickeditem[0][2], clickeditem[0][3], clickeditem[0][4], clickeditem[0][5], clickeditem[0][6], clickeditem[0][7], clickeditem[0][8], clickeditem[0][9],)
            cursor.execute(sql, vals)
        else:
            maxpid = "SELECT PID FROM ProductHistory WHERE link='%s'" % clickeditem[0][9]
            cursor.execute(maxpid)
            maxpid = cursor.fetchall()
            maxpid = maxpid[0][0]

        #updates the links clicked table
        sql = "SELECT EXISTS(SELECT * FROM LinksClicked WHERE PID=%s)"
        vals = (maxpid,)
        cursor.execute(sql, vals)
        item = cursor.fetchall()
        #if item is found in links clicked table
        if(item[0][0]!=0):
            sql = "UPDATE LinksClicked SET clicked=clicked+1 WHERE PID=%s" % (maxpid)
            cursor.execute(sql)
        else:
            sql = "INSERT INTO LinksClicked(PID, addr, clicked) VALUES(%s, %s, %s)"
            vals = (maxpid, str(ip), 1,)
            cursor.execute(sql, vals)

        cursor.close()
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        cursor.close()
        conn.close()
        return "FAILED: %s %s" % (str(sys.exc_info()[2].tb_lineno), str(sys.exc_info()))
