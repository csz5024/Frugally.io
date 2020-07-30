from flask import Flask, session, render_template, request, redirect, Response, url_for
from flaskext.mysql import MySQL
from flask_restful import Resource, Api
import logging
import html
from PIL import Image
import requests
from bs4 import BeautifulSoup
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


app = Flask(__name__)
api = Api(app)

'''

All code is original and written by Casey Zduniak, 2020

Use app.logger.info() to log information to the flask.log file in the same directory. use like a normal print statement

This file is organized into APP ROUTES, FILTERS, and MAIL SENDER subheadings

'''
'''

:::'###::::'########::'########:::::'########:::'#######::'##::::'##:'########:'########::'######::
::'## ##::: ##.... ##: ##.... ##:::: ##.... ##:'##.... ##: ##:::: ##:... ##..:: ##.....::'##... ##:
:'##:. ##:: ##:::: ##: ##:::: ##:::: ##:::: ##: ##:::: ##: ##:::: ##:::: ##:::: ##::::::: ##:::..::
'##:::. ##: ########:: ########::::: ########:: ##:::: ##: ##:::: ##:::: ##:::: ######:::. ######::
 #########: ##.....::: ##.....:::::: ##.. ##::: ##:::: ##: ##:::: ##:::: ##:::: ##...:::::..... ##:
 ##.... ##: ##:::::::: ##::::::::::: ##::. ##:: ##:::: ##: ##:::: ##:::: ##:::: ##:::::::'##::: ##:
 ##:::: ##: ##:::::::: ##::::::::::: ##:::. ##:. #######::. #######::::: ##:::: ########:. ######::
..:::::..::..:::::::::..::::::::::::..:::::..:::.......::::.......::::::..:::::........:::......:::

'''

#logging.basicConfig(filename='Flask.log', level=logging.INFO)


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


# Lets us know which product the user clicked on, then redirects them to the site
@app.route('/redirect/<possibleArgs>/<path:plink>')
def perm_redirect(possibleArgs, plink):
    if(possibleArgs == "www.nike.com" or possibleArgs == "nordstromrack.com"):
        product = possibleArgs+'/'+plink
    else:
        app.logger.info(possibleArgs)
        possibleArgs = possibleArgs.replace("-","%2F")
        #possibleArgs = html.escape(possibleArgs)
        product = plink+"?"+possibleArgs
    ipaddr = request.remote_addr
    # use product link as primary key (should we switch to product IDs?)
    # associate the IP address with the product link

    # check if item is sold out
    page = requests.get("https://"+product)
    soup = BeautifulSoup(page.content, 'html.parser')
    if(len(soup.find_all("div", class_="status-badge--sold-out"))>=1):
        #this item is sold out
        #delete it from the Frugally DB
        errorval = DBqueries.deleteSoldOut(str(product).strip())
        app.logger.info("Sold Out error: %s" % errorval)
        return redirect(session['prevLink'], code=301)
    else:
        app.logger.info("%s: Link Clicked: %s | %s" % (datetime.now(),ipaddr,product))
        errorval = DBqueries.Collect(product, ipaddr)
        app.logger.info(errorval)
        return redirect("https://"+product, code=301)


# landing page
@app.route('/home', methods=['GET'])
def index():

    #app.logger.info("Index")
    nordstrom = DBqueries.getSQLNordstrom()
    nike = DBqueries.getSQLNike()
    fullList = nordstrom + nike
    items = len(fullList)
    itemsinrow = 3
    itemsperpage = 16
    page = 0
    brands = getBrands(fullList)
    vendors = ["Nordstrom", "Nike"]

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page=itemsperpage, total=items//itemsinrow+1, css_framework='bootstrap3')

    session['prevLink'] = "https://frugally.io/home"
    return render_template('index.html', objects=fullList, itemsinrow=itemsinrow, items=items, pagination=pagination, brands=brands, vendors=vendors)


# post methods for homepage
@app.route('/home', methods=['POST'])
def feedback():

    formid = request.form.get("homepage","")

    app.logger.info("Post received")
    # Send email
    if(formid == "2"):

        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # sends to gmail
        sendMail(email, name, message)
        return redirect('https://frugally.io/home', code=302)
    else:
    	return redirect("https://frugally.io/home", code=302)


@app.route('/', methods=["GET", "POST"])
def about():

    #POST
    if(request.method == 'POST'):
        formid = request.form.get("aboutpage","")

        # Send email (gmail disabled our account for some reason)
        if(formid == "2"):

            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            # sends to gmail
            sendMail(email, name, message)

    session['prevLink'] = "https://frugally.io/"
    return render_template('about.html')


'''
The following contains two url paths, one for men, and one for women

<filters> is a dynamic route that acts as a url variable, containing various info
'''
@app.route('/men/<filters>', methods=["GET", "POST"])
def men(filters):

    #POST
    if(request.method == 'POST'):
        formid = request.form.get("menspage","")

        # Send email
        if(formid == "2"):

            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            # sends to gmail
            sendMail(email, name, message)

        elif(formid == "1"):
            radio = request.form.get('radio')
            vendorfilter = request.form.getlist('vendorsBox')
            brands = request.form.getlist('brandsBox')
            prange = request.form.getlist('rangeBox')
            return returnFilter(radio, vendorfilter, brands, prange, "men")
    #GET
    else:
        session['prevLink'] = "https://frugally.io/men/"+filters
        options = parseFilter(filters)
        #app.logger.info(options)
        objects, errorlogger = DBqueries.getSQLsort(options, gender='men')
        #app.logger.info(errorlogger)
        maxprice = round(DBqueries.getMaxPriceMen())
        itemsinrow = 3
        items = len(objects)
        itemsperpage = 16
        page = 0
        brands = getBrands(objects)
        prange = getPrices(maxprice)
        vendors = ["Nordstrom Rack", "Nike"]

        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, per_page=itemsperpage, total=items//itemsinrow+1, css_framework='bootstrap3')

        return render_template('mens.html', objects=objects, itemsinrow=itemsinrow, items=items, pagination=pagination, brands=brands, vendors=vendors, prange=prange)
    return redirect('https://frugally.io/home', code=302)


@app.route('/women/<filters>', methods=["GET", "POST"])
def women(filters):
    #POST
    if(request.method == 'POST'):
        formid = request.form.get("womenspage","")

        # Send email
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
            prange = request.form.getlist('rangeBox')
            return returnFilter(radio, vendorfilter, brands, prange, "women")
    else:
        session['prevLink'] = "https://frugally.io/women/"+filters
        options = parseFilter(filters)
        objects, errorlogger = DBqueries.getSQLsort(options, gender='women')
        #app.logger.info(errorlogger)
        maxprice = round(DBqueries.getMaxPriceWomen())
        items = len(objects)
        itemsinrow = 3
        itemsperpage = 16
        page = 0
        brands = getBrands(objects)
        prange = getPrices(maxprice)
        vendors = ["Nordstrom Rack", "Nike"]

        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, per_page=itemsperpage, total=items//itemsinrow+1, css_framework='bootstrap3')

        return render_template('womens.html', objects=objects, itemsinrow=itemsinrow, items=items, pagination=pagination, brands=brands, vendors=vendors, prange=prange)
    return redirect('https://frugally.io/home', code=302)


#login page (unused at the moment)
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

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



'''
'########:'####:'##:::::::'########:'########:'########:::'######::
 ##.....::. ##:: ##:::::::... ##..:: ##.....:: ##.... ##:'##... ##:
 ##:::::::: ##:: ##:::::::::: ##:::: ##::::::: ##:::: ##: ##:::..::
 ######:::: ##:: ##:::::::::: ##:::: ######::: ########::. ######::
 ##...::::: ##:: ##:::::::::: ##:::: ##...:::: ##.. ##::::..... ##:
 ##:::::::: ##:: ##:::::::::: ##:::: ##::::::: ##::. ##::'##::: ##:
 ##:::::::'####: ########:::: ##:::: ########: ##:::. ##:. ######::
..::::::::....::........:::::..:::::........::..:::::..:::......:::

'''

# https://frugally.io/men/sort=discout+vendors=nordstromrack+brands=asics_guess+pr=

# The packing and unpacking URL filters
def returnFilter(radio, vendors, brands, prange, gender):
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
        filterstring = filterstring+"+range="
        for i in prange:
           filterstring = filterstring+str(i)+"_"
        if(filterstring[-1] != "="):
            filterstring = filterstring[:-1]
        return redirect(("https://frugally.io/"+gender+"/"+filterstring), code=302)
    except:
        return redirect("https://frugally.io", code=302)


def parseFilter(filter):
    options = filter.split('+')
    if((len(options) <= 1) or (filter == 'home')):
        return [['sort', 'discount'], ['vendors', 'all'], ['brands', 'all'], ['range', 'all']]
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
        if(values[-1][0] == 'range'):
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

# This gathers price ranges to be output in the filters menu
def getPrices(maxprice):
    mprices = ["$0-$100"]
    for i in range((maxprice//100)):
        mprices.append("$%s00-$%s00" % (str(i+1), str(i+2)))

    return mprices


'''
'##::::'##::::'###::::'####:'##:::::::::::'######::'########:'##::: ##:'########::'########:'########::
 ###::'###:::'## ##:::. ##:: ##::::::::::'##... ##: ##.....:: ###:: ##: ##.... ##: ##.....:: ##.... ##:
 ####'####::'##:. ##::: ##:: ##:::::::::: ##:::..:: ##::::::: ####: ##: ##:::: ##: ##::::::: ##:::: ##:
 ## ### ##:'##:::. ##:: ##:: ##::::::::::. ######:: ######::: ## ## ##: ##:::: ##: ######::: ########::
 ##. #: ##: #########:: ##:: ##:::::::::::..... ##: ##...:::: ##. ####: ##:::: ##: ##...:::: ##.. ##:::
 ##:.:: ##: ##.... ##:: ##:: ##::::::::::'##::: ##: ##::::::: ##:. ###: ##:::: ##: ##::::::: ##::. ##::
 ##:::: ##: ##:::: ##:'####: ########::::. ######:: ########: ##::. ##: ########:: ########: ##:::. ##:
..:::::..::..:::::..::....::........::::::......:::........::..::::..::........:::........::..:::::..::

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

# Setter and Getter class object used as a pseudo global variable
class previousPage:
    def __init__(self, link=None):
        self._link = link

    def get_Link(self):
        return self._link

    def set_Link(self, x):
        self._link = x


if __name__ == '__main__':
    prevLink = previousPage()
    app.run(ssl_context=('/var/www/Frugally/frugally.io-ssl-bundle/domain.cert.pem', '/var/www/Frugally/frugally.io-ssl-bundle/private.key.pem'))
