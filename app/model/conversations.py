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
        return f'<Conversations {self.username}>'

    def soft_delete(self):
        """Marks the user as deleted by setting the deleted_at timestamp."""
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    @classmethod
    def query_active(cls, *args, **kwargs):
        """Return only active (non-soft-deleted) users."""
        return cls.query.filter(cls.deleted_at == None, *args, **kwargs)