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
    
    

@chats_bp.route('/chats/<int:chat_id>', methods=['GET'])
@jwt_required()
def get_chat_with_conversation(chat_id):
    try:
        user_id = get_jwt_identity()
        
        # Fetch the chat by ID
        chat = Chats.query.filter_by(id=chat_id).first()
        
        if not chat:
            return jsonify({'message': "No chat found"}), 404
        
        # Fetch the associated conversation for this chat
        conversation = Conversations.query.filter_by(id=chat.conversations_id).first()
        
        if not conversation:
            return jsonify({'message': "No conversation found for this chat"}), 404
        
        # Prepare the response data
        

        conversation_data = {
            'id': conversation.id,
            'summary': conversation.summary,
            'user_id':conversation.user_id,
            'created_at': conversation.created_at
        }

        chat_data = {
            'question': chat.questions,
            'answer': chat.answer,
            'created_at': chat.created_at,
            'id':chat.id,
            "conversation":conversation_data
        }

        # Return the chat and its associated conversation details
        return jsonify(chat_data), 200
        
    except Exception as e:
        return jsonify({"message": "An error occurred", "info": str(e)}), 500
