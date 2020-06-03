from flask import Flask
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'GjHPucpWicgF9jVmKOQ1s31xunFbjuY3ir3O9yMhoYpz2K6N2ktFvQ' # this is for security; on terminal, can import secrets, then run secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ucsf_da.db'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)

'''
app = flask.Flask(__name__)
app.secret_key = 'fuzzybuddy'

mysql = MySQL()
mysql.init_app(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = input('MySQL Password: ')
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'ucsfda'

'''
import tracking_tool.views
