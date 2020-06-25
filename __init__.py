from flask import Flask, render_template, request, redirect, Response, url_for
from flaskext.mysql import MySQL
from PIL import Image
import requests
import json
from io import BytesIO
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
#from threading import Timer
import operator
import locale
from flask_paginate import Pagination, get_page_parameter
from flask_bootstrap import Bootstrap
import mysql.connector
import sys
sys.path.append("..")
from Frugally import DBqueries

conn = mysql.connector.connect(
    host="localhost",
    user="frugally",
    password="Shoelas",
    database="Frugally"
)

app = Flask(__name__)


'''

All code is original and written by Casey Zduniak, 2020

Use app.logger.info() to log information to the flask.log file in the same directory. use like a normal print statement


'''


# This section upgrades http requests to https
@app.before_request
def before_request():
    if(request.url.startswith('http://')):
        url = request.url.replace('http://', 'https://', 1)
        #app.logger.info("HTTPS redirect")
        return redirect(url,code=301)


# Custom Internal Server Error Page 
@app.errorhandler(500)
def InternalError(e):
    return render_template('500.html'), 500


# landing page
@app.route('/', methods=['GET'])
def index():

    #nordstrom = getNordstromContent()
    nordstrom = getSQLNordstrom()
    #nike = getNikeContent()
    nike = getSQLNike()
    fullList = nordstrom + nike
    items = len(fullList)
    itemsinrow = 3
    itemsperpage = 16
    page = 0
    brands = getBrands(fullList)
    vendors = ["Nordstrom", "Nike"]

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page=itemsperpage, total=items//itemsinrow+1, css_framework='bootstrap3')

    return render_template('index.html', objects=fullList, itemsinrow=itemsinrow, items=items, pagination=pagination, brands=brands, vendors=vendors)


#this is for google only
@app.route('/google5e9dcfe4850ad995.html')
def google():
    return render_template('google5e9dcfe4850ad995.html')


#robots.txt
@app.route('/robots.txt', methods=['GET'])
def robots():
    with open('/var/www/Frugally/Frugally/templates/robots.txt', 'r') as f:
        content = f.read()
    return Response(content, mimetype='text')


#sitemap
@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []
    deltadays = datetime.now() - timedelta(days=7)
    deltadays = deltadays.strftime("%Y-%m-%d")

    for rule in app.url_map.iter_rules():
        if 'GET' in rule.methods and len(rule.arguments) == 0 and not rule.rule.startswith('/admin'):
            pages.append([ url_for('index', _external=True) + rule.rule, deltadays])

    sitemap_template = render_template('sitemap.xml', pages=pages)
    response = Response(sitemap_template)
    response.headers["Content-Type"] = "application/xml"
    return response



# post methods for homepage
@app.route('/', methods=['POST'])
def feedback():

    formid = request.form.get("homepage","")

    # Send email
    if(formid == "2"):

        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # sends to gmail
        sendMail(email, name, message)
        return redirect('http://frugally.io', code=302)

    elif(formid == "1"):
        #radio = request.form.get('radio')
        #gender = request.form.get('radio2')
        #vendorfilter = request.form.getlist('vendorsBox')
        #brands = request.form.getlist('brandsBox')
        #app.logger.info(brands)
        return returnFilter(radio='discount', vendorfilter='all', brands='all')

    else:
    	return redirect("http://frugally.io", code=302)


'''
The following contains two url paths, one for men, and one for women

<filters> is a dynamic route that acts as a url variable, containing various info
'''
@app.route('/men/<filters>', methods=["GET", "POST"])
def men(filters):

    #POST
    if(request.method == 'POST'):
        formid = request.form.get("homepage","")

        # Send email (gmail disabled our account for some reason)
        if(formid == "2"):

            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            # sends to gmail
            sendMail(email, name, message)

        elif(formid == "1"):
            radio = request.form.get('radio')
            #gender = request.form.get('radio2')
            vendorfilter = request.form.getlist('vendorsBox')
            brands = request.form.getlist('brandsBox')
            return returnFilter(radio, vendorfilter, brands)
    else:
        options = parseFilter(filters)
        #nordstrom = getNordstromContent()
        #nike = getNikeContent()
        nordstrom = getSQLNordstrom()
        nike = getSQLNike()
        #objects = getSort(nordstrom+nike, options, gender='men')
        itemsinrow = 3
        items = len(objects)
        itemsperpage = 16
        page = 0
        brands = getBrands(objects)
        vendors = ["Nordstrom", "Nike"]

        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, per_page=itemsperpage, total=items//itemsinrow+1, css_framework='bootstrap3')

        return render_template('mens.html', objects=objects, itemsinrow=itemsinrow, items=items, pagination=pagination, brands=brands, vendors=vendors)
    return redirect('https://frugally.io', code=302)

@app.route('/women/<filters>', methods=["GET", "POST"])
def women(filters):
    #POST
    if(request.method == 'POST'):
        formid = request.form.get("homepage","")

        # Send email (gmail disabled our account for some reason)
        if(formid == "2"):

            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            # sends to gmail
            sendMail(email, name, message)

        elif(formid == "1"):
            radio = request.form.get('radio')
            #gender = request.form.get('radio2')
            vendorfilter = request.form.getlist('vendorsBox')
            brands = request.form.getlist('brandsBox')
            return returnFilter(radio, vendorfilter, brands)
    else:
        options = parseFilter(filters)
        nordstrom = getNordstromContent()
        nike = getNikeContent()
        objects = getSort(nordstrom+nike, options, gender='women')
        items = len(objects)
        itemsinrow = 3
        itemsperpage = 16
        page = 0
        brands = getBrands(objects)
        vendors = ["Nordstrom", "Nike"]

        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, per_page=itemsperpage, total=items//itemsinrow+1, css_framework='bootstrap3')

        return render_template('womens.html', objects=objects, itemsinrow=itemsinrow, items=items, pagination=pagination, brands=brands, vendors=vendors)
    return redirect('https://frugally.io', code=302)


#login page (unused at the moment)
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


# The packing and unpacking URL filters
def returnFilter(radio, vendors, brands):
    try:
        if(radio == None):
            radio = 'discount'
        else:
            radio = radio.lower()
        filterstring = "sort="+radio+"+vendors="
        for i in vendors:
           filterstring = filterstring+str(i)+"_"
        if(filterstring[-1] != '='):
            filterstring = filterstring[:-1]
        filterstring=filterstring+"+brands="
        for i in brands:
           filterstring = filterstring+str(i)+"_"
        if(filterstring[-1] != "="):
            filterstring = filterstring[:-1]
        return redirect(("http://frugally.io/"+filterstring), code=302)
    except:
        return redirect("http://frugally.io", code=302)

def parseFilter(filter):
    options = filter.split('+')
    if((len(options) <= 1) or (filter == 'home')):
        return [['sort', 'discount'], ['vendors', 'all'], ['brands', 'all']]
    values = []
    #app.logger.info(options)
    for i in options:
        values.append(i.split('='))
        if(values[-1][0] == 'vendors'):
            if(len(values[-1][1]) <= 1):
                values[-1][1] = "all"
            else:
                vends = values[-1].pop(-1)
                values[-1].append(vends.split('_'))
        if(values[-1][0] == 'brands'):
            if(len(values[-1][1]) <= 1):
                values[-1][1] = "all"
            else:
                brands = values[-1].pop(-1)
                values[-1].append(brands.split('_'))
        #app.logger.info(values)
    return values


# This just gathers the list of brands to be displayed in the filter menu
def getBrands(objects):
    brands = []
    for i in objects:
        if(i[3] not in brands):
            if(i[3] != None):
                brands.append(i[3])
    brands.sort()
    return brands

'''
#wrapper function for getDiscount and getPrice
def getSort(products, options, gender):
    app.logger.info(options)
    sortmethod = options.pop(0)
    sortmethod = sortmethod[1]
    options.insert(0,['gender', str(gender)])
    app.logger.info(options)
    if(sortmethod == 'discount'):
        objects = getDiscount(products, options)
    elif(sortmethod == 'low'):
        objects = getPrice(products, options, highlow=False)
    else:
        objects = getPrice(products, options, highlow=True)
    return objects

# This function ultimatley gets the best discounts with the specified filters
def getDiscount(products, filters):
    #filters is now an array [[gender, m/f], [vendor, [nike, nordstrom]], [brand, [burberry, guess, ...]]]
    objects = []
    if(filters!=None):
        gender = str(filters[0][1]).lower()
        filtervendor = filters[1][1]
        filterbrands = filters[2][1]
    else:
        gender = "all"
        filtervendor = "all"
        filterbrands = "all"

    app.logger.info(gender+" "+filtervendor+" "+filterbrands)
    counter=0 # used to keep track of the actual products to be displayed (dont use i)
    for i in range(len(products)):
        item = products[i].__dict__

        # Filters out the undesired products
        if(gender != "all"):
            if((item["gender"]==None)or(item["gender"].lower()!=gender)):
                continue
        if(filtervendor != "all"):
            if(item["vendor"] not in filtervendor):
                continue
        if(filterbrands != "all"):
            if(item["brand"] not in filterbrands):
                continue

        # adds products to objects array
        if(item["vendor"] == "Nike"):
            #nike
            objects.append(listing())
            objects[counter].setVendor(item["vendor"])
            objects[counter].setName(item["name"])
            if(item["price"]!=None):
                price=item["price"]
            else:
                price = "$0"
            objects[counter].setPrice(price)
            if((item["original"]!=None) and (item["price"]!=None)):
                retail = float(item["original"][1:])
                price = float(item["price"][1:])
                discount = int(round((1-(price/retail))*100))
            else:
                discount = 0
            objects[counter].setDiscount(discount)
            objects[counter].setBrand(item["brand"])
            objects[counter].setOriginal(item["original"])
            objects[counter].setLink(item["link"].strip('https://'))
            objects[counter].setImg(item["img"])
            objects[counter].setGender(item["gender"])
            counter+=1
        elif(item["vendor"] == "Nordstrom Rack"):
            #nordstrom
            objects.append(listing())
            objects[counter].setVendor("Nordstrom Rack")
            objects[counter].setName(item["name"])
            objects[counter].setPrice(item["price"])
            if(item["discount"] != None):
                dis = item["discount"].split("%")
                dis = int(dis[0])
            else:
                dis = 0
            objects[counter].setDiscount(dis)
            objects[counter].setBrand(item["brand"])
            objects[counter].setOriginal(item["original"])
            objects[counter].setLink(item["link"])
            objects[counter].setImg(item["img"])
            objects[counter].setGender(item["gender"])
            counter+=1

    # sort by best discount
    objects.sort(key=operator.attrgetter('discount'), reverse=True)
    for i in objects:
        i.setDiscount(str(i.discount) + "%")

    return objects


def getPrice(products, filters, highlow):
    #filters is now an array [[gender, m/f], [vendor, [nike, nordstrom]]]
    #highlow is a boolean that determines the sort order
    objects = []
    if(filters!=None):
        gender = str(filters[0][1])
        filtervendor = filters[1][1]
        filterbrands = filters[2][1]
    else:
        gender = "all"
        filtervendor = "all"
        filterbrands = "all"

    counter=0
    for i in range(len(products)):
        item = products[i].__dict__

        if(gender != "all"):
            if((item["gender"]==None)or(item["gender"].lower()!=gender)):
                continue
        if(filtervendor != "all"):
            if(item["vendor"] not in filtervendor):
                continue
        if(filterbrands != "all"):
            if(item["brand"] not in filterbrands):
                continue

        if(item["vendor"] == "Nike"):
            #nike
            objects.append(listing())
            objects[counter].setVendor(item["vendor"])
            objects[counter].setName(item["name"])
            if(item["price"]!=None):
                if(len(item["price"][1:]) > 6):
                    price = float(item["price"][1:].replace(',',''))
                else:
                    price = float(item["price"][1:])
            else:
                price = 0
            objects[counter].setPrice(price)
            if((item["original"]!=None) and (item["price"]!=None)):
                retail = float(item["original"][1:])
                price = float(item["price"][1:])
                discount = int(round((1-(price/retail))*100))
            else:
                discount = 0
            objects[counter].setDiscount(str(discount))
            objects[counter].setBrand(item["brand"])
            objects[counter].setOriginal(item["original"])
            objects[counter].setLink(item["link"].strip('https://'))
            objects[counter].setImg(item["img"])
            objects[counter].setGender(item["gender"])
            counter+=1
        elif(item["vendor"] == "Nordstrom Rack"):
            #nordstrom
            objects.append(listing())
            objects[counter].setVendor("Nordstrom Rack")
            objects[counter].setName(item["name"])
            if(item["price"] != None):
                if(len(item["price"][1:]) > 6):
                    price = float(item["price"][1:].replace(',',''))
                else:
                    price = float(item["price"][1:])
            else:
                price = 0
            objects[counter].setPrice(price)
            if(item['discount'] != None):
                disc = item["discount"]
            else:
                disc = "-0%"
            objects[counter].setDiscount(disc)
            objects[counter].setBrand(item["brand"])
            objects[counter].setOriginal(item["original"])
            objects[counter].setLink(item["link"])
            objects[counter].setImg(item["img"])
            objects[counter].setGender(item["gender"])
            counter+=1

    objects.sort(key=operator.attrgetter('price'), reverse=highlow)
    for i in objects:
        if(i.price == 0):
            i.setPrice("See Price in Cart")
        else:
            i.setPrice("$"+str(i.price))

    return objects
'''

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

'''
# Populates product listings
def getNordstromContent():
    objects = []
    with open('/var/www/Frugally/Frugally/nordstromracksales/NordstromRackMen.json') as f:
        data = json.load(f)

    counter = 0
    for count, item in enumerate(data):
        objects.append(listing())
        objects[count].setName(item["title"])
        objects[count].setPrice(item["price"])
        if(item['discount'] != None):
            disc = item["discount"].split()
        else:
            disc = "-0%"
        objects[count].setDiscount(disc[0])
        objects[count].setBrand(item["brand"])
        objects[count].setOriginal(item["retail-price"])
        objects[count].setLink("nordstromrack.com"+item["link"])
        objects[count].setImg(item["image-link"])
        objects[count].setVendor("Nordstrom Rack")
        objects[count].setGender(item["gender"])
        counter+=1

    f.close()
    with open('/var/www/Frugally/Frugally/nordstromracksales/NordstromRackWomen.json') as f:
        data = json.load(f)

    for count, item in enumerate(data):
        objects.append(listing())
        objects[counter].setName(item["title"])
        objects[counter].setPrice(item["price"])
        if(item['discount'] != None):
            disc = item["discount"].split()
        else:
            disc = "-0%"
        objects[counter].setDiscount(disc[0])
        objects[counter].setBrand(item["brand"])
        objects[counter].setOriginal(item["retail-price"])
        objects[counter].setLink("nordstromrack.com"+item["link"])
        objects[counter].setImg(item["image-link"])
        objects[counter].setVendor("Nordstrom Rack")
        objects[counter].setGender(item["gender"])
        counter+=1

    app.logger.info("Nordstrom objects loaded: "+str(len(objects)))
    f.close()
    return objects

def getNikeContent():
    objects = []
    with open('/var/www/Frugally/Frugally/nordstromracksales/NikeMen.json') as f:
        data = json.load(f)

    counter = 0
    for count, item in enumerate(data):
        objects.append(listing())
        objects[count].setName(item["title"])
        objects[count].setPrice(item["price"])
        if((item["retail-price"]!=None) and (item["price"]!=None)):
            retail = float(item["retail-price"].strip("$"))
            price = float(item["price"].strip("$"))
            discount = round((1-(price/retail))*100)
        else:
            discount = 0
        objects[count].setDiscount(str(discount))
        objects[count].setBrand(item["brand"])
        objects[count].setOriginal(item["retail-price"])
        objects[count].setLink(item["link"].strip('https://'))
        objects[count].setImg(item["image-link"])
        objects[count].setVendor(item["vendor"])
        objects[count].setGender(item["gender"])
        counter+=1

    f.close()
    with open('/var/www/Frugally/Frugally/nordstromracksales/NikeWomen.json') as f:
        data = json.load(f)

    for count, item in enumerate(data):
        objects.append(listing())
        objects[counter].setName(item["title"])
        objects[counter].setPrice(item["price"])
        if((item["retail-price"]!=None) and (item["price"]!=None)):
            retail = float(item["retail-price"].strip("$"))
            price = float(item["price"].strip("$"))
            discount = round((1-(price/retail))*100)
        else:
            discount = 0
        objects[counter].setDiscount(str(discount))
        objects[counter].setBrand(item["brand"])
        objects[counter].setOriginal(item["retail-price"])
        objects[counter].setLink(item["link"].strip('https://'))
        objects[counter].setImg(item["image-link"])
        objects[counter].setVendor(item["vendor"])
        objects[counter].setGender(item["gender"])
        counter+=1

    app.logger.info('Nike objects loaded: '+str(len(objects)))
    f.close()
    return objects
'''

# Sends email from burner gmail to frugally gmail
def sendMail(customer, name, message):
    user = 'frugallyserver@gmail.com'
    pw = 'z4M<c2=3W:n;Fg@^'
    recv = 'frugallyio@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recv
    msg['Subject'] = 'Website Feedback'
    body = '%s at %s\n\n%s\n\nSent from Frugally Application Server' % (name, customer, message)
    msg.attach(MIMEText(body))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #server.ehlo()
    server.login(user, pw)
    server.sendmail(user, recv, msg.as_string())
    server.quit()
    return 'success'

'''
# Product listing object
class listing:
    def __init__(self):
        self.img = None
        self.name = None
        self.brand = None
        self.price = None
        self.original = None
        self.discount = None
        self.link = None
        self.vendor = None
        self.gender = None

    def setImg(self, img):
        self.img = img

    def setName(self, name):
        self.name = name

    def setBrand(self, brand):
        self.brand = brand

    def setPrice(self, price):
        self.price = price

    def setOriginal(self, original):
        self.original = original

    def setDiscount(self, discount):
        self.discount = discount

    def setLink(self, link):
        self.link = link

    def setVendor(self, vendor):
        self.vendor = vendor
`
    def setGender(self, gender):
        self.gender = gender
'''

if __name__ == '__main__':
    app.run(ssl_context=('/var/www/Frugally/frugally.io-ssl-bundle/domain.cert.pem', '/var/www/Frugally/frugally.io-ssl-bundle/private.key.pem'), debug=True)
