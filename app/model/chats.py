from datetime import datetime
from app.pre_require import db

class Chats(db.Model):
    __tablename__="chats"
    id = db.Column(db.Integer, primary_key=True)
    questions= db.Column(db.String, nullable=False)
    answer= db.Column(db.String, nullable=True)
    conversations_id= db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    # conversation_instance = db.relationship('Conversations', backref='chat_ref', lazy=True)

    def __repr__(self):
        return f'<Chats {self.username}>'
    
    def to_dict(self):
        """Convert the Conversation object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "questions": self.questions,
            "answer": self.answer,
            "conversations_id": self.conversations_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }

    def soft_delete(self):
        """Marks the user as deleted by setting the deleted_at timestamp."""
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    @classmethod
    def query_active(cls, *args, **kwargs):
        """Return only active (non-soft-deleted) users."""
        return cls.query.filter(cls.deleted_at == None, *args, **kwargs)