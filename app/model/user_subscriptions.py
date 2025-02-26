from datetime import datetime
from app.pre_require import db

class User_Subscriptions(db.Model):
    __tablename__='user_subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    checkout_id = db.Column(db.String, nullable=False)
    amount = db.Column(db.String, nullable=False)
    create_time = db.Column(db.String, nullable=False)
    expire_time = db.Column(db.String, nullable=False)
    payment_status = db.Column(db.String, nullable=False)
    subscription_id = db.Column(db.String, nullable=False)
    invoice_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User_Subscriptions {self.checkout_id}>'
    
    def to_dict(self):
        """Convert the Conversation object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "checkout_id": self.checkout_id,
            "amount": self.amount,
            "create_time": self.create_time,
            "expire_time": self.expire_time,
            "payment_status": self.payment_status,
            "subscription_id":self.subscription_id,
            "invoice_id":self.invoice_id,
            "user_id": self.user_id,
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