from tracking_tool import db, login_manager
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # columns for table
    username = username = db.Column(db.String(45), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    id = db.Column(db.Integer, primary_key = True) # primay_key indicates unique identifier

    def __repr__(self): # how object is printed
        return f"User('{self.username}', '{self.email}')"

