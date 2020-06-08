from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

# this is for security; on terminal, can import secrets, then run secrets.token_hex(16)
app.config['SECRET_KEY'] = 'GjHPucpWicgF9jVmKOQ1s31xunFbjuY3ir3O9yMhoYpz2K6N2ktFvQ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:00krusty*@localhost/ucsfda'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)

import tracking_tool.views

