from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.model.users import User
from app.model.user_subscriptions import User_Subscriptions
import stripe
import os
from app.pre_require import db

stripe.api_key = os.getenv("STRIPE_SECRET_KEYS")
user_sub_bp = Blueprint('user_sub_bp', __name__)

#cs_test_a1giprHub3Si4zWuTF8VHOJYXM9s5HAjXpBsQZMQAI180AJnQ3qCeKSgZp

@user_sub_bp.route('/subscriptions/user/create', methods=['POST'])
@jwt_required()
def create_subscription():
    try:
        data=request.get_json()
        user_id = get_jwt_identity()

        user_data = User.query.filter_by(id=user_id).first()

        session = stripe.checkout.Session.create(
            success_url="http://localhost:5173/success?session_id={CHECKOUT_SESSION_ID}",
            line_items=[{"price": data["price_id"], "quantity": 1}],
            mode="subscription",
            customer=user_data.stripe_customer_id
        )

        return jsonify({"clientSecret":session.client_secret, "session":session}), 200
    except Exception as e:
        return jsonify({"message":"Procedure failed","info":str(e)}), 500
    
@user_sub_bp.route('/subscriptions/user/get', methods=['POST'])
@jwt_required()
def get_subscription():
    try:
        data=request.get_json()
        user_id = get_jwt_identity()

        user_data = User.query.filter_by(id=user_id).first()

        session = stripe.checkout.Session.retrieve(
                    data["session_id"],
                )
        
        get_user_sub_data = User_Subscriptions.query.filter_by(checkout_id=data["session_id"]).first()

        if not get_user_sub_data:
            user_sub = User_Subscriptions(checkout_id=session.id, amount=session.amount_total,create_time=session.created,expire_time=session.expires_at,payment_status=session.payment_status,subscription_id=session.subscription, invoice_id=session.invoice, user_id=user_id)
            try:
                db.session.add(user_sub)
                db.session.commit()
                return jsonify({"session":session, "sub_data":None, "message":"Subscription created successfully"}),200
            except Exception as e:
                db.session.rollback()
                return jsonify({"message":"Procedure failed","info":str(e)}), 500
        else:
            return jsonify({"session":session, "sub_data":None, "message":"Subscription Already added"}),200
    except Exception as e:
        return jsonify({"message":"Procedure failed","info":str(e)}), 500