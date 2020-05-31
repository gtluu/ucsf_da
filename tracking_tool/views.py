import flask
from tracking_tool import *
from flaskext.mysql import MySQL
import flask_login


class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.id = None
        self.auth = None

    def authenticate(self):
        cur = mysql.connect().cursor()
        cur.execute("SELECT username, password, salt, id, authorization FROM users WHERE username = '" +
                    self.username + "'")
        results = cur.fetchone()
        if results:
            username, password, salt, id, authorization = results
            cur.close()
            self.password = hashlib.sha512(self.password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
            if self.username == username and self.password == password:
                self.id = id
                self.auth = int(authorization)
                return True
        else:
            cur.close()
            return False


def check_session(page, data):
    try:
        if flask.session['logged_in']:
            if data:
                return flask.render_template(page, data=data)
            else:
                return flask.render_template(page)
        else:
            return flask.render_template('index.html')
    except KeyError:
        return flask.render_template('index.html')


@app.route('/')
def main():
    return flask.render_template('index.html')


@app.route('/login')
def login_page():
    return flask.render_template('index.html')


@app.route('/home', methods=['POST'])
def login():
    form = flask.request.form.to_dict()

    flask.session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    user = User(form['username'], form['password'])

    if user.authenticate():
        flask.session['access'] = user.auth
        flask.session['logged_in'] = True
        if flask.session['access'] == 0:
            return check_session('su_home.html', None)
        elif flask.session['access'] == 1:
            return check_session('admin_home.html', None)
        elif flask.session['access'] == 2:
            return check_session('advisor_home.html', None)
        elif flask.session['access'] == 3:
            return check_session('student_home.html', None)
        elif flask.session['access'] == 4:
            return check_session('parent_home.html', None)
        else:
            # no access to page
            return flask.render_template('account_inactive.html')
    else:
        return flask.render_template('index.html')


@app.route('/register')
def registration_page():
    return flask.render_template('register.html')


@app.route('/registernewuser', methods=['POST'])
def register():
    form = flask.request.form.to_dict()
    if form['password'] != form['password_re']:
        return flask.render_template('registration_password_mismatch.html')

    query = 'INSERT INTO users (id, authorization, ucsf_da_id, username, salt, password) VALUES '
    con = mysql.connect()
    cur = con.cursor()
    # generate system user id
    cur.execute('SELECT id FROM users')
    id_list = cur.fetchall()
    id_list = [i[0] for i in id_list]
    while True:
        id = random.randint(100000, 999999)
        if id not in id_list:
            break

    # set authorization level
    # 0 == su, 1 == admin, 2 == advisor, 3 == student, 4 == parent, 5 == inactive
    cur.execute('SELECT id FROM admins')
    admin_id_list = cur.fetchall()
    admin_id_list = [int(i[0]) for i in admin_id_list]
    cur.execute('SELECT id FROM advisors')
    advisor_id_list = cur.fetchall()
    advisor_id_list = [int(i[0]) for i in advisor_id_list]
    cur.execute('SELECT id FROM students')
    student_id_list = cur.fetchall()
    student_id_list = [int(i[0]) for i in student_id_list]
    cur.execute('SELECT id FROM parents')
    parent_id_list = cur.fetchall()
    parent_id_list = [int(i[0]) for i in parent_id_list]
    is_admin = int(form['id']) in admin_id_list
    is_advisor = int(form['id']) in advisor_id_list
    is_student = int(form['id']) in student_id_list
    is_parent = int(form['id']) in parent_id_list
    if is_admin and not is_advisor and not is_student and not is_parent:
        auth = 1
    elif is_advisor and not is_admin and not is_student and not is_parent:
        auth = 2
    elif is_student and not is_admin and not is_advisor and not is_parent:
        auth = 3
    elif is_parent and not is_admin and not is_advisor and not is_student:
        auth = 4
    else:
        auth = 5

    # get salt
    salt = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(128))
    # encode password
    password = hashlib.sha512(form['password'].encode('utf-8') + salt.encode('utf-8')).hexdigest()

    # add to users database
    values = (str(id), str(auth), str(form['id']), "'" + form['username'] + "'", "'" + salt + "'", "'" + password + "'")
    query += '(' + ', '.join(values) + ');'
    cur.execute(query)
    con.commit()
    cur.close()
    return flask.render_template('registration_complete.html')


@app.route('/forms')
def forms():
    if flask.session['access'] <= 2:
        return check_session('forms.html', None)
    else:
        return flask.render_template('restricted_message.html')


@app.route('/new_student_form')
def new_student_form():
    if flask.session['access'] <= 2:
        return check_session('new_student_form.html', None)
    else:
        return flask.render_template('restricted_message.html')


@app.route('/student_status_change')
def student_status_change():
    if flask.session['access'] <= 2:
        return check_session('student_status_change.html', None)
    else:
        return flask.render_template('restricted_message.html')


@app.route('/students')
def students():
    if flask.session['access'] <= 2:
        con = mysql.connect()
        cur = con.cursor()
        cur.execute('SELECT * FROM admins')
        data = cur.fetchall()
        return check_session('students.html', data)
    else:
        return flask.render_template('restricted_message.html')


@app.route('/logout')
def logout():
    flask.session['logged_in'] = False
    flask.session.pop('username', None)
    return flask.render_template('index.html')
