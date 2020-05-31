import flask
from flaskext.mysql import MySQL
from tracking_tool import *
from datetime import timedelta
import random
import string
import hashlib


app = flask.Flask(__name__)
app.secret_key = 'fuzzybuddy'

mysql = MySQL()
mysql.init_app(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = input('MySQL Password: ')
<<<<<<< HEAD
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
=======
app.config['MYSQL_DATABSE_HOST'] = 'localhost'
>>>>>>> 13450fe9fbb7639f0d2bbf615f504909f0c1851a
app.config['MYSQL_DATABASE_DB'] = 'ucsfda'


import tracking_tool.views
