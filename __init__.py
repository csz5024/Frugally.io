from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    objects = [None, None, None]
    objects[0] = listing(None, None, None, None)
    objects[1] = listing(None, None, None, None)
    objects[2] = listing(None, None, None, None)
    objects[0].setImg('static/images/pic01.jpg')
    objects[1].setImg('static/images/pic02.jpg')
    objects[2].setImg('static/images/pic03.jpg')
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
    app.run(debug=True)
