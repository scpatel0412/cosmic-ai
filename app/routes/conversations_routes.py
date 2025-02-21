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


@conversations_bp.route('/conversations/<int:id>', methods=['GET'])
@jwt_required()
def get_conversation(id):
    try:
        # Fetch the conversation by its ID
        conversation = Conversations.query.get(id)
        
        # If conversation not found, return 404
        if not conversation:
            return jsonify({"message": "Conversation not found"}), 404

        # Get associated chats for the conversation
        chats = [{
            'id': chat.id,
            'questions': chat.questions,
            'answer': chat.answer,
            'created_at':chat.created_at,
            'updated_at':chat.updated_at
        } for chat in conversation.chat_ref]
        
        # Prepare response data
        response_data = {
            'id': conversation.id,
            'summary': conversation.summary,
            'user_id': conversation.user_id,
            'created_at': conversation.created_at,
            'updated_at': conversation.updated_at,
            'deleted_at': conversation.deleted_at,
            'chats': chats
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"message": "Procedure failed", "info": str(e)}), 500

@conversations_bp.route('/conversations/user/all', methods=['GET'])
@jwt_required()
def get_all_converdations():
    try:
        user_id = int(get_jwt_identity())
        print(user_id)
        
        conversations = Conversations.query.filter_by(user_id=user_id).all()
        print(conversations)
        # return ""
        return jsonify({"data":[conversation.to_dict() for conversation in conversations]}),200
    except Exception as e:
        return jsonify({"message": "Procedure failed", "info": str(e)}), 500