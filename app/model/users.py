from datetime import datetime
from app.pre_require import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), unique=True, nullable=False)
    email = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    first_name = db.Column(db.String(500), nullable=False)
    last_name = db.Column(db.String(500), nullable=False)
    contact = db.Column(db.String(500), nullable=False)
    stripe_customer_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    conversations = db.relationship('Conversations', backref='users', lazy=True)
    user_subscriptions = db.relationship('User_Subscriptions')

    def __repr__(self):
        return f'<User {self.username}>'

    def soft_delete(self):
        """Marks the user as deleted by setting the deleted_at timestamp."""
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    @classmethod
    def query_active(cls, *args, **kwargs):
        """Return only active (non-soft-deleted) users."""
        return cls.query.filter(cls.deleted_at == None, *args, **kwargs)
