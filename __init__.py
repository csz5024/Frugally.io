from flask import Flask, render_template
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
    pass

# Populates product listings
def getContent(objects):
    # os library is not working for some reason
    
    #os.getcwd()
    #os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #os.chdir("static")
    #os.chdir("images")
    #os.chdir("dump")

    # the absolute path on the server. 
    dir = "/var/www/Frugally/Frugally/static/images/dump"
    for count, filename in enumerate(os.listdir(dir)):
        objects.append(listing(None, None, None, None))
        objects[count].setImg('static/images/dump/' + filename)
    objects[0].setName("Commes Des Garcons")
    objects[0].setPrice("$100.00")
    objects[0].setDiscount("(33% off MSRP)")
    return objects

# Product listing object
class listing:
    def __init__(self, img, name, price, discount):
        self.img = img
        self.name = name
        self.price = price
        self.discount = discount

    def setImg(self, img):
        self.img = img

    def setName(self, name):
        self.name = name

    def setPrice(self, price):
        self.price = price

    def setDiscount(self, discount):
        self.discount = discount

if __name__ == '__main__':
    app.run()
