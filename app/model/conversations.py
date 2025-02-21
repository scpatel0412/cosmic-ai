from datetime import datetime
from app.pre_require import db

class Conversations(db.Model):
    __tablename__="conversations"
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    user = db.relationship('User')
    chat_ref = db.relationship('Chats', backref='conversation_instance', lazy=True)

    def __repr__(self):
        return f'<Conversations {self.user.username}>'

    def soft_delete(self):
        """Marks the user as deleted by setting the deleted_at timestamp."""
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        """Convert the Conversation object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "summary": self.summary,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "user": {
                "id": self.user.id,
                "username": self.user.username  # Assuming `User` model has a `username` field
            }
        }

    @classmethod
    def query_active(cls, *args, **kwargs):
        """Return only active (non-soft-deleted) users."""
        return cls.query.filter(cls.deleted_at == None, *args, **kwargs)