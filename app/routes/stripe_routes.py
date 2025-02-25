from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import stripe
import os

stripe_bp = Blueprint('stripe_bp', __name__)

stripe.api_key = os.getenv("STRIPE_SECRET_KEYS")

@stripe_bp.route('/stripe/products', methods=['GET'])
def get_stripe_product():
    try:
        data=stripe.Product.list(limit=3)
        return jsonify(data),200
    except Exception as e:
        return jsonify({"message": "An error occurred", "info": str(e)}), 500

@stripe_bp.route('/stripe/products/<string:id>', methods=['GET'])
def get_stripe_product_by_id(id):
    try:
        data=stripe.Product.retrieve(id)
        return jsonify({"data":data}),200
    except Exception as e:
        return jsonify({"message": "An error occurred", "info": str(e)}), 500

@stripe_bp.route('/stripe/prices', methods=['GET'])
def get_stripe_price():
    try:
        data=stripe.Price.list(limit=3)
        return jsonify(data),200
    except Exception as e:
        return jsonify({"message": "An error occurred", "info": str(e)}), 500

@stripe_bp.route('/stripe/prices/<string:id>', methods=['GET'])
def get_stripe_price_by_id(id):
    try:
        data=stripe.Price.retrieve(id)
        return jsonify({"data":data}),200
    except Exception as e:
        return jsonify({"message": "An error occurred", "info": str(e)}), 500

@stripe_bp.route('/stripe/complete/products', methods=['GET'])
def get_stripe_complete_product():
    try:
        data=stripe.Product.list(limit=3)
        for i in range(0,len(data.data)):
            data1 = stripe.Price.retrieve(data.data[i].default_price)
            data.data[i]["price_details"]=data1
        return jsonify(data),200
    except Exception as e:
        return jsonify({"message": "An error occurred", "info": str(e)}), 500
    
@stripe_bp.route('/stripe/complete/products/<string:product_id>', methods=['GET'])
def get_stripe_complete_product_by_id(product_id):
    try:
        data = stripe.Product.retrieve(product_id)
        data1 = stripe.Price.retrieve(data.default_price)
        data["price_details"]=data1
           
        return jsonify({"data":data}),200
    except Exception as e:
        return jsonify({"message": "An error occurred", "info": str(e)}), 500
