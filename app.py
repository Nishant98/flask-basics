from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    # constructor
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

# Product Schema
class ProductSchema(ma.Schema):
    # fields to show
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')


# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Create Product
@app.route("/product", methods=["POST"])
def addProduct():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    quantity = request.json["quantity"]

    newProduct = Product(name, description, price, quantity)
    db.session.add(newProduct)
    db.session.commit()

    return product_schema.jsonify(newProduct)

# Get All Products
@app.route("/products", methods=["GET"])
def getProducts():
    allProducts = Product.query.all()
    result = products_schema.dump(allProducts)

    return jsonify(result)

# Get A Product
@app.route("/product/<id>", methods=["GET"])
def getProduct(id):
    product = Product.query.get(id)

    return product_schema.jsonify(product)


# Update Product
@app.route("/product/<id>", methods=["PUT"])
def updateProduct(id):
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    quantity = request.json["quantity"]

    product = Product.query.get(id)

    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    db.session.commit()

    return product_schema.jsonify(product)

# Delete Product
@app.route("/product/<id>", methods=["DELETE"])
def deleteProduct(id):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return "Successfully Deleted Product {}".format(product.name)

# Home Page
@app.route("/", methods=["GET"])
def renderHome():
    return render_template('home.html')


@app.errorhandler(404)
def handle_404(e):
    # handle all other routes here
    return "Not Found, but we HANDLED IT"
    
# Run Server
if __name__ == "__main__":
    app.run(debug=True)
