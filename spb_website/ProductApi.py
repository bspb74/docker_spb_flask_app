from flask.views import MethodView
from flask_smorest import Blueprint, abort
import marshmallow as ma
from flask_jwt_extended import jwt_required
from flask import json


from app import db
from models import Product

api_product = Blueprint("ProductAPI", __name__, url_prefix='/api/v1', description="Product API")


class ProductSchema(ma.Schema):
    model = ma.fields.String()
    prodName = ma.fields.String()
    prodType = ma.fields.String()
    imgName = ma.fields.String()
    price = ma.fields.Decimal()
    prodDesc = ma.fields.String()
    stockQty = ma.fields.Int()


@api_product.route("/products")
class ProductsAPI(MethodView):

    @jwt_required()
    @api_product.doc(security=[{"Bearer Auth": []}])
    @api_product.response(200, ProductSchema(many=True))
    def get(self):
        items = Product.query.all()
        return items


@api_product.route("/product/insert")
class ProductAddAPI(MethodView):

    @jwt_required()
    @api_product.doc(security=[{"Bearer Auth": []}])
    @api_product.arguments(ProductSchema)
    @api_product.response(201, ProductSchema, description="Add A New Product")
    def post(self, product_data):
        """Create New Product"""
        print(f"Product Name: {product_data["prodName"]}")
        product = Product(
            model=product_data["model"],
            prodName=product_data["prodName"],
            prodType=product_data["prodType"],
            imgName=product_data["imgName"],
            price=product_data["price"],
            prodDesc=product_data["prodDesc"],
            stockQty=product_data["stockQty"]
        )
        try:
            db.session.add(product)
            db.session.commit()
        except Exception as e:
            print(f"Error adding procuct to DB:\n%s" % e)

        return product


@api_product.route("/product/delete/<string:prod_name>")
class ProductAPIDeleteProduct(MethodView):

    @jwt_required()
    @api_product.doc(security=[{"Bearer Auth": []}])
    @api_product.response(201, ProductSchema)
    def post(self, prod_name):
        item = Product.query.filter_by(prodName=prod_name).first()
        print(f"Product Name: {item.prodName}")
        print(item)
        prod_id = item.id
        print(f"Prodcut ID: {prod_id}")
        Product.query.filter_by(id=prod_id).delete()
        db.session.commit()


@api_product.route("/product/model/<string:prod_model>")
class ProductApi(MethodView):

    @jwt_required()
    @api_product.doc(security=[{"Bearer Auth": []}])
    @api_product.response(200, ProductSchema(many=True))
    def get(self, prod_model):
        print("Product ID: %s" % prod_model)
        item = Product.query.filter_by(model=f"{prod_model}")
        return item


@api_product.route("/product/name/<string:prod_name>")
class ProductApi(MethodView):

    @jwt_required()
    @api_product.doc(security=[{"Bearer Auth": []}])
    @api_product.response(200, ProductSchema(many=True))
    def get(self, prod_name):
        print("Product ID: %s" % prod_name)
        item = Product.query.filter_by(prodName=f"{prod_name}")
        return item


@api_product.route("/product/type/<string:prod_type>")
class ProductApi(MethodView):
    @jwt_required()
    @api_product.doc(security=[{"Bearer Auth": []}])
    @api_product.response(200, ProductSchema(many=True))
    def get(self, prod_type):
        print("Product ID: %s" % prod_type)
        item = Product.query.filter_by(prodType=f"{prod_type}")
        return item