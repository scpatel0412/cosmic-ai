from flask import Blueprint, jsonify, request
from app.pre_require import db
from datetime import timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.model import Conversations

conversations_bp = Blueprint('conversations_bp', __name__)

@conversations_bp.route('/conversations/create', methods=['POST'])
@jwt_required()
def create_converstation():
    # data = request.get_json()
    try:
        user_id = get_jwt_identity()
        new_conversation = Conversations(summary="test", user_id=user_id)
        db.session.add(new_conversation)
        db.session.commit()
        return jsonify({'id': new_conversation.id, 'summary': new_conversation.summary}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":"Procedure failed","info":str(e)}), 500
