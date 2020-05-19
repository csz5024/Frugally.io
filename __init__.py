from flask import Flask, render_template
from PIL import Image
import requests
import json
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/')
def index():
    objects = []
    itemsinrow = 3
    objects = getContent(objects)
    items = len(objects)
    return render_template('index.html', objects=objects, itemsinrow=itemsinrow, items=items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

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
        objects[count].setLink(item["link"])

        #images and links are not right in json
        #objects[count].setImg(grabImage(item["image-link"]))

    return objects

# grabs image from url
def grabImage(link):
    response = requests.get(link)
    img = Image.open(BytesIO(response.content))
    return img

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
    app.run(debug=True)
