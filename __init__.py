from flask import Flask, render_template, request, redirect
from PIL import Image
import requests
import json
from io import BytesIO
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from threading import Timer
import operator
import locale
from flask_paginate import Pagination, get_page_parameter
from flask_bootstrap import Bootstrap

app = Flask(__name__)

@app.before_request
def before_request():
    if(request.url.startswith('http://')):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        app.logger.info("HTTPS redirect")
        return redirect(url,code=code)


@app.route('/')
def index():

    obj = objectsArray()
    itemsinrow = 3
    obj.setNordstrom(getNordstromContent())
    obj.setNike(getNikeContent())
    nordstrom = obj.getNordstrom()
    nike = obj.getNike()
    fullList = nordstrom + nike
    items = len(fullList)
    itemsperpage = 16
    page = 0
    brands = getBrands(fullList)
    vendors = ["Nordstrom", "Nike"]

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page=itemsperpage, total=items//itemsinrow+1, css_framework='bootstrap3')

    return render_template('index.html', objects=fullList, itemsinrow=itemsinrow, items=items, pagination=pagination, brands=brands, vendors=vendors)



@app.route('/', methods=['POST'])
def feedback():

    formid = request.form.get("homepage","")

    # Send email (gmail disabled our account for some reason)
    if(formid == "2"):

        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # sends to gmail
        sendMail(email, name, message)
        return redirect('http://frugally.io', code=302)

    elif(formid == "1"):
        radio = request.form.get('radio')
        gender = request.form.get('radio2')
        vendorfilter = request.form.getlist('vendors')
        return returnFilter(radio, gender, vendorfilter)

    else:
    	return redirect("http://frugally.io", code=302)


@app.route('/low/<filters>', methods=["GET", "POST"])
def sortLow(filters):

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
            gender = request.form.get('radio2')
            vendorfilter = request.form.getlist('vendors')
            return returnFilter(radio, gender, vendorfilter)
    else:
        options = parseFilter(filters)
        nordstrom = getNordstromContent()
        nike = getNikeContent()
        itemsinrow = 3
        objects = getLowPrice(nordstrom+nike, options)
        items = len(objects)
        itemsperpage = 16
        page = 0
        brands = getBrands(objects)
        vendors = ["Nordstrom", "Nike"]

        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, per_page=itemsperpage, total=items//itemsinrow+1, css_framework='bootstrap3')

        return render_template('index.html', objects=objects, itemsinrow=itemsinrow, items=items, pagination=pagination, brands=brands, vendors=vendors)
    return redirect('https://frugally.io', code=302)

@app.route('/high/<filters>', methods=["GET", "POST"])
def sortHigh(filters):
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
            gender = request.form.get('radio2')
            vendorfilter = request.form.getlist('vendors')
            return returnFilter(radio, gender, vendorfilter)
    else:
        options = parseFilter(filters)
        nordstrom = getNordstromContent()
        nike = getNikeContent()
        itemsinrow = 3
        objects = getHighPrice(nordstrom+nike, options)
        items = len(objects)
        itemsperpage = 16
        page = 0
        brands = getBrands(objects)
        vendors = ["Nordstrom", "Nike"]

        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, per_page=itemsperpage, total=items//itemsinrow+1, css_framework='bootstrap3')

        return render_template('index.html', objects=objects, itemsinrow=itemsinrow, items=items, pagination=pagination, brands=brands, vendors=vendors)
    return redirect('https://frugally.io', code=302)

@app.route('/discount/<filters>', methods=["GET", "POST"])
def sortDiscount(filters):

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
            gender = request.form.get('radio2')
            vendorfilter = request.form.getlist('vendors')
            return returnFilter(radio, gender, vendorfilter)
    else:
        app.logger.info("Discount here")
        options = parseFilter(filters)
        nordstrom = getNordstromContent()
        nike = getNikeContent()
        itemsinrow = 3
        objects = getDiscount(nordstrom+nike, options)
        items = len(objects)
        itemsperpage = 16
        page = 0
        brands = getBrands(objects)
        vendors = ["Nordstrom", "Nike"]

        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, per_page=itemsperpage, total=items//itemsinrow+1, css_framework='bootstrap3')

        return render_template('index.html', objects=objects, itemsinrow=itemsinrow, items=items, pagination=pagination, brands=brands, vendors=vendors)
    return redirect('https://frugally.io', code=302)

#login page (unused)
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

#Filters
def returnFilter(radio, gender, vendors):
    try:
        radio = radio.lower()
        filterstring = "gender="+gender+"+vendors="
        for i in vendors:
           filterstring = filterstring+i+"_"
        return redirect("http://frugally.io/"+radio+"/"+filterstring, code=302)
    except:
        return redirect("http://frugally.io", code=302)

def parseFilter(filter):
    with open('/var/www/Frugally/Frugally/debug.json', 'w') as outfile:
        json.dump({"filter": str(filter)}, outfile)
    options = filter.split('%2B')
    values = []
    for i in options:
        values.append(i.split('%3D'))
        if(values[-1][0] == 'vendors'):
            vends = values[-1].pop(-1)
            values[-1].append(vends.split('_'))
    return values


#IMPORTANT must be used after one of the other filters (objects should already be populated)
def getBrands(objects):
    brands = []
    for i in objects:
        if(i.brand not in brands):
            if(i.brand != None):
                brands.append(i.brand)
    brands.sort()
    return brands

def getDiscount(products, filters):
    #filters is now an array [[gender, m/f], [vendor, [nike, nordstrom]]]
    objects = []
    if(filters!=None):
        gender = filters[0][1]
        vendors = filters[1][1]
        filtervendor = "all"
        #otherwise show all products
        if(len(vendors)<2):
            if(len(vendors) == 1):
                filtervendor = vendors[0]
            else:
                filtervendor = "all"
    else:
        gender = "all"
        filtervendor = "all"
    if(filtervendor != "all"):
        if(filtervendor.lower() == "nike"):
            products = getNikeContent()
        else:
            products = getNordstromContent()
    for count, item in enumerate(products):
        if(gender != "all"):
            if(item["gender"].lower()!=gender):
                continue

        data = {}
        data['item'] = []
        data['enum'] = []
        data['item'].append(str(products[0].__dict__))
        data['enum'].append(str(item.__dict__))
        with open('/var/www/Frugally/Frugally/debug.json', 'w') as outfile:
            json.dump(data, outfile)
        if(item["vendor"] == "Nike"):
            #nike
            objects.append(listing())
            objects[count].setVendor(item["vendor"])
            objects[count].setName(item["title"])
            if(item["price"]!=None):
                price=item["price"]
            else:
                price = "$0"
            objects[count].setPrice(price)
            if((item["retail-price"]!=None) and (item["price"]!=None)):
                retail = float(item["retail-price"][1:])
                price = float(item["price"][1:])
                discount = int(round((1-(price/retail))*100))
            else:
                discount = 0
            objects[count].setDiscount(discount)
            objects[count].setBrand(item["brand"])
            objects[count].setOriginal(item["retail-price"])
            objects[count].setLink(item["link"])
            objects[count].setImg(item["image-link"])
            objects[count].setGender(item["gender"])
        elif(item["vendor"] == "NordstromRack"):
            #nordstrom
            objects.append(listing())
            objects[count].setVendor(item["vendor"])
            objects[count].setName(item["title"])
            objects[count].setPrice(item["price"])
            if(item["discount"] != None):
                dis = item["discount"].split("%")
                dis = int(dis[0])
            else:
                dis = 0
            objects[count].setDiscount(dis)
            objects[count].setBrand(item["brand"])
            objects[count].setOriginal(item["retail-price"])
            objects[count].setLink("nordstromrack.com"+item["link"])
            objects[count].setImg(item["image-link"])
            objects[count].setGender(item["gender"])

    objects.sort(key=operator.attrgetter('discount'), reverse=True)
    for i in objects:
        i.setDiscount(str(i.discount) + "%")

    return objects

def getHighPrice(products, filters):
    #filters is now an array [[gender, m/f], [vendor, [nike, nordstrom]]]
    objects = []
    if(filters!=None):
        gender = filters[0][1]
        vendors = filters[1][1]
        filtervendor = "all"
        #otherwise show all products
        if(len(vendors)<2):
            if(len(vendors) == 1):
                filtervendor = vendors[0]
            else:
                filtervendor = "all"
    else:
        gender = "all"
        filtervendor = "all"
    if(filtervendor != "all"):
        if(filtervendor.lower() == "nike"):
            products = getNikeContent()
        else:
            products = getNordstormContent()
    for count, item in enumerate(products):
        if(gender != "all"):
            if(item["gender"].lower()!=gender):
                continue
        objects.append(listing())
        objects[count].setVendor(item["vendor"])
        if(item["vendor"] == "Nike"):
            #nike
            objects[count].setName(item["title"])
            if(item["price"]!=None):
                if(len(item["price"][1:]) > 6):
                    price = float(item["price"][1:].replace(',',''))
                else:
                    price = float(item["price"][1:])
            else:
                price = 0
            objects[count].setPrice(price)
            if((item["retail-price"]!=None) and (item["price"]!=None)):
                retail = float(item["retail-price"][1:])
                price = float(item["price"][1:])
                discount = int(round((1-(price/retail))*100))
            else:
                discount = 0
            objects[count].setDiscount(str(discount))
            objects[count].setBrand(item["brand"])
            objects[count].setOriginal(item["retail-price"])
            objects[count].setLink(item["link"])
            objects[count].setImg(item["image-link"])
            objects[count].setGender(item["gender"])
        elif(item["vendor"] == "NordstromRack"):
            #nordstrom
            objects[count].setName(item["title"])
            if(item["price"] != None):
                if(len(item["price"][1:]) > 6):
                    price = float(item["price"][1:].replace(',',''))
                else:
                    price = float(item["price"][1:])
            else:
                price = 0
            objects[count].setPrice(price)
            if(item['discount'] != None):
                disc = item["discount"].split()
            else:
                disc = "-0%"
            objects[count].setDiscount(disc[0])
            objects[count].setBrand(item["brand"])
            objects[count].setOriginal(item["retail-price"])
            objects[count].setLink("nordstromrack.com"+item["link"])
            objects[count].setImg(item["image-link"])
            objects[count].setGender(item["gender"])

    objects.sort(key=operator.attrgetter('price'), reverse=True)
    for i in objects:
        if(i.price == 0):
            i.setPrice("See Price in Cart")
        else:
            i.setPrice("$"+str(i.price))

    return objects

def getLowPrice(products, filters):
    #filters is now an array [[gender, m/f], [vendor, [nike, nordstrom]]]
    objects = []
    if(filters!=None):
        gender = filters[0][1]
        vendors = filters[1][1]
        filtervendor = "all"
        #otherwise show all products
        if(len(vendors)<2):
            if(len(vendors) == 1):
                filtervendor = vendors[0]
            else:
                filtervendor = "all"
    else:
        gender = "all"
        filtervendor = "all"
    if(filtervendor != "all"):
        if(filtervendor.lower() == "nike"):
            products = getNikeContent()
        else:
            products = getNordstromContent()
    for count, item in enumerate(products):
        if(gender != "all"):
            if(item["gender"].lower()!=gender):
                continue
        objects.append(listing())
        if(item["vendor"] == "Nike"):
            #nike
            objects[count].setName(item["title"])
            if(item["price"]!=None):
                if(len(item["price"][1:]) > 6):
                    price = float(item["price"][1:].replace(',',''))
                else:
                    price = float(item["price"][1:])
            else:
                price = 0
            objects[count].setPrice(price)
            if((item["retail-price"]!=None) and (item["price"]!=None)):
                retail = float(item["retail-price"][1:])
                price = float(item["price"][1:])
                discount = int(round((1-(price/retail))*100))
            else:
                discount = 0
            objects[count].setDiscount(str(discount))
            objects[count].setBrand(item["brand"])
            objects[count].setOriginal(item["retail-price"])
            objects[count].setLink(item["link"])
            objects[count].setImg(item["image-link"])
            objects[count].setGender(item["gender"])
            objects[count].setVendor(item["vendor"])
        elif(item["vendor"] == "NordstromRack"):
            #nordstrom
            objects[count].setName(item["title"])
            if(item["price"] != None):
                if(len(item["price"][1:]) > 6):
                    price = float(item["price"][1:].replace(',',''))
                else:
                    price = float(item["price"][1:])
            else:
                price = 0
            objects[count].setPrice(price)
            if(item['discount'] != None):
                disc = item["discount"].split()
            else:
                disc = "-0%"
            objects[count].setDiscount(disc[0])
            objects[count].setBrand(item["brand"])
            objects[count].setOriginal(item["retail-price"])
            objects[count].setLink("nordstromrack.com"+item["link"])
            objects[count].setImg(item["image-link"])
            objects[count].setGender(item["gender"])
            objects[count].setVendor(item["vendor"])

    objects.sort(key=operator.attrgetter('price'))
    for i in objects:
        if(i.price == 0):
            i.setPrice("See Price in Cart")
        else:
            i.setPrice("$"+str(i.price))

    return objects

# Populates product listings
def getNordstromContent():
    objects = []
    with open('/var/www/Frugally/Frugally/nordstromracksales/NordstromRackMen.json') as f:
        data = json.load(f)

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
        objects[count].setVendor(item["vendor"])
        objects[count].setGender(item["gender"])

    with open('/var/www/Frugally/Frugally/nordstromracksales/NordstromRackWomen.json') as f:
        data = json.load(f)

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
        objects[count].setVendor(item["vendor"])
        objects[count].setGender(item["gender"])

    return objects

def getNikeContent():
    objects = []
    with open('/var/www/Frugally/Frugally/nordstromracksales/NikeMen.json') as f:
        data = json.load(f)

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
        objects[count].setLink(item["link"])
        objects[count].setImg(item["image-link"])
        objects[count].setVendor(item["vendor"])
        objects[count].setGender(item["gender"])

    with open('/var/www/Frugally/Frugally/nordstromracksales/NikeWomen.json') as f:
        data = json.load(f)

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
        objects[count].setLink(item["link"])
        objects[count].setImg(item["image-link"])
        objects[count].setVendor(item["vendor"])
        objects[count].setGender(item["gender"])

    return objects


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


# NEED TO FIX: updates the product listing daily at 3am
def globalTimer():
    x = datetime.today()
    y = x.replace(day=x.day, hour=3, minute=0, second=0, microsecond=0) + timedelta(days=1)
    delta_t=y-x

    secs = delta_t.total_seconds()

    def updateContent():
        os.system("cd /var/www/Frugally/Frugally/nordstromracksales")
        os.system("sudo rm NordstromRack.json")
        os.system("sudo scrapy crawl NordstromRack -o NordstromRack.json")
        return "success"

    t = Timer(secs, updateContent)
    t.start()

# Big container of product listings
class objectsArray:
    def __init__(self):
        self.nordstrom = None
        self.nike = None

    def setNordstrom(self, objects):
        self.nordstrom = objects

    def getNordstrom(self):
        return self.nordstrom

    def setNike(self, objects):
        self.nike = objects

    def getNike(self):
        return self.nike

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

    def setGender(self, gender):
        self.gender = gender


if __name__ == '__main__':
    globalTimer()
    app.run(ssl_context=('/var/www/Frugally/frugally.io-ssl-bundle/domain.cert.pem', '/var/www/Frugally/frugally.io-ssl-bundle/private.key.pem'), debug=True)
