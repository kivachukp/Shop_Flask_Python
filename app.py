from flask import Flask, render_template, request
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from cloudipsp import Api, Checkout
# api = Api(merchant_id=1396424,
#           secret_key='test')
# checkout = Checkout(api=api)
# data = {
#     "currency": "USD",
#     "amount": 10000
# }
# url = checkout.url(data).get('checkout_url')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/last')
def last():
    return render_template('last.html')

@app.route('/create', methods=['POST','GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']
        item = Item(title=title, price=price, text=text)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Произошла ошибка'
    else:
        return render_template('create.html')

class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    text = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<{self.title} %r>'%self.id
with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run(debug=True)
