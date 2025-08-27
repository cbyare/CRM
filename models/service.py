from datetime import datetime
from models import db

class Services(db.Model):
    __tablename__ = 'services'
    ServiceId = db.Column(db.Integer, primary_key=True)
    ServiceName = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.Text)
    ServiceTime = db.Column(db.DateTime)
    
    # Relationships
    subscriptions = db.relationship('Subscription', backref='service', lazy=True)
    transactions = db.relationship('Transaction', backref='service', lazy=True)
