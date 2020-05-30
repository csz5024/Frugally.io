from flask import Flask, render_template, request, redirect
from PIL import Image
import requests
import json
from io import BytesIO
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from datetime import datetime, timedelta
from threading import Timer

app = Flask(__name__)

@app.route('/')
def index():

    objects = []
    itemsinrow = 3
    objects = getContent(objects)
    items = len(objects)

    return render_template('index.html', objects=objects, itemsinrow=itemsinrow, items=items)



@app.route('/', methods=['POST'])
def feedback():

    # from the suggestions box in footer

    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    data = {}
    data['name'] = name
    data['email'] = email
    data['message'] = message

    # sends to gmail
    sendMail(email, name, message)
    #status = sendMail(email, name, message)
    #data['status'] = status

    # appends suggestions to json file
    '''
    with open('/var/www/Frugally/Frugally/Suggestions.json') as jfile:
        old = json.load(jfile)
        tmp = old
        tmp.append(data)

    with open('/var/www/Frugally/Frugally/Suggestions.json', 'w') as outfile:
        json.dump(tmp, outfile, indent=4)
    '''
    return redirect("http://frugally.io", code=302)


#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


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


# Populates product listings
def getContent(objects):

    #os.getcwd()
    #os.chdir("scraping")

    with open('/var/www/Frugally/Frugally/scraping/NordstromRack.json') as f:
        data = json.load(f)

    for count, item in enumerate(data):
        objects.append(listing())
        objects[count].setName(item["title"])
        objects[count].setPrice(item["price"])
        objects[count].setDiscount(item["discount"])
        objects[count].setBrand(item["brand"])
        objects[count].setOriginal(item["retail-price"])
        objects[count].setLink("nordstromrack.com"+item["link"])

        #images and links are not right in json
        objects[count].setImg(item["image-link"])

    return objects

# updates the product listing daily at 3am
def globalTimer():
    x = datetime.today()
    y = x.replace(day=x.day, hour=3, minute=0, second=0, microsecond=0) + timedelta(days=1)
    delta_t=y-x

    secs = delta_t.total_seconds()

    def updateContent():
        os.system("cd /var/www/Frugally/Frugally/scraping")
        os.system("sudo rm NordstromRack.json")
        os.system("sudo scrapy crawl NordstromRack -o NordstromRack.json")
        return "success"

    t = Timer(secs, updateContent)
    t.start()


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



if __name__ == '__main__':
    globalTimer()
    app.run(debug=True)
