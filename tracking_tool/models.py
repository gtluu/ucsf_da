from tracking_tool import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
# check if User authenticated, active, annonymous, get ID
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    # columns for table

    username = db.Column(db.String(45), unique=True, nullable = False)
    password = db.Column(db.String(60), nullable=False)
    authorization = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True)  # primay_key indicates unique identifier

    def __repr__(self): # how object is printed
        return f"User('{self.username}')"

