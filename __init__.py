from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    objects = [one, two, three]
    return render_template('index.html', objects=objects)

class listing:
    def __init__(self, img, name, price, discount):
        self.img = img
        self.name = name
        self.price = price
        self.discount = discount

    def setImg(self, img):
        self.img = img


if __name__ == '__main__':
    one = listing(None, None, None, None)
    two = listing(None, None, None, None)
    three = listing(None, None, None, None)
    one.setImg('static/images/pic01.jpg')
    two.setImg('static/images/pic02.jpg')
    three.setImg('static/images/pic03.jpg')
    app.run(debug=True)
