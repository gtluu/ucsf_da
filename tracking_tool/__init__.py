import flask
from  flaskext.mysql import MySQL


app = flask.Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = input('MySQL Password: ')
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABSE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'ucsfda'


import tracking_tool.views
