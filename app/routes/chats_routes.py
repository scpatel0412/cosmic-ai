from flask import Blueprint, jsonify, request
from app.pre_require import db
from datetime import timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.model import Conversations, Chats
from app.service import Groq_Service

chats_bp = Blueprint('chats_bp', __name__)

@chats_bp.route('/chats/create', methods=['POST'])
@jwt_required()
def create_chat():
    try:
        data=request.get_json()
        user_id= get_jwt_identity()
        get_conversation = Conversations.query.filter_by(id=data['conv_id']).first()

        if not get_conversation:
            return jsonify({'message':"No conversation found"}), 404
        
        groq = Groq_Service()

        message = groq.get_answer(data['question'])

        try:
            new_chat = Chats(questions=data['question'], conversations_id=data['conv_id'],answer = message.content)
            db.session.add(new_chat)
            db.session.commit()
            return jsonify({'message':message.content,"question":new_chat.questions}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message":"Procedure failed","info":str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":"Procedure failed","info":str(e)}), 500
    
    

