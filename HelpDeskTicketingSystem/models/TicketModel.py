from ..extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    estimated_time = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', backref='tickets')