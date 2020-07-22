# This file will be used as an import for __init__.py containing all of the SQL queries
import mysql.connector
'''
conn = mysql.connector.connect(
    host="localhost",
    user="frugally",
    password="Shoelas20",
    database="Frugally"
)
cursor = conn.cursor()
'''
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


def collect(link, userid):
    conn = mysql.connector.connect(
        host="localhost",
        user="frugally",
        password="Shoelas20",
        database="BigData"
    )
    cursor = conn.cursor()

    cursor.execute('INSERT INTO LinksClicked(PID, UserID, url) VALUES(%s, %s, %s);', (NULL, str(userid), link))

    item = cursor.fetchall()

    cursor.close()
    conn.close()
    return item
