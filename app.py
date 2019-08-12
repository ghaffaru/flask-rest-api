from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#init app
app = Flask(__name__)

# @app.route('/')
# def home():
#     return jsonify({'name':'ghaff'})
basedir = os.path.abspath(os.path.dirname(__file__))

#databse
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)

#init marshmallow
ma = Marshmallow(app)

#Product class or model
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self,name,description,price,quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

#product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','quantity')

#init schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True,strict=True)

#create a product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    new_product = Product(name,description,price,quantity)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


#Run server
if __name__ == '__main__':
    app.run(debug=True)

