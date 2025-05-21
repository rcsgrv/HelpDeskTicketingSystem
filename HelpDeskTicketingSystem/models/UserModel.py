from ..extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    forename = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    account_type = db.Column(db.String(20), nullable=False)
    tickets = db.relationship('Ticket')