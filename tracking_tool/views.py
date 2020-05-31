import flask
from tracking_tool import app, MySQL


@app.route('/')
def main():
    return flask.render_template('index.html')


@app.route('/login')
def login_page():
    return flask.render_template('index.html')


@app.route('/loginnewuser', methods=['POST'])
def login():
    form = flask.request.form.to_dict()
    # replace with checking user id and password in sql database
    # password hashing/salting
    if form['username'] == '' and form['password'] == '':
        return flask.render_template('advisor_home.html')
    else:
        return flask.render_template('index.html')


@app.route('/register')
def registration_page():
    return flask.render_template('register.html')


@app.route('/registrationnewuser', methods=['POST'])
def register():
    form = flask.request.form.to_dict()
    # replace with checking user id and password in sql database
    # password hashing/salting
    # create new user in db
    pass


@app.route('/advisor_home')
def advisor_home():
    return flask.render_template('advisor_home.html')


@app.route('/forms')
def forms():
    return flask.render_template('forms.html')


@app.route('/new_student_form')
def new_student_form():
    return flask.render_template('new_student_form.html')


@app.route('/student_status_change')
def student_status_change():
    return flask.render_template('student_status_change.html')


@app.route('/students')
def students():
    return flask.render_template('students.html')
