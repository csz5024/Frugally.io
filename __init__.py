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
    Directory = os.getcwd() + "/"
    for count, filename in enumerate(os.listdir(Directory)):
        objects.append(listing(None, None, None, None))
        objects[count].setImg('static/images/dump/' + filename)
    objects[0].setName("Air Force 1s")
    objects[0].setPrice("$100.00")
    objects[0].setDiscount("(20% off MSRP)")
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
    # changes working directory to dump so that the product listings can be pushed
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("static")
    os.chdir("images")
    os.chdir("dump")
    app.run(debug=True)
