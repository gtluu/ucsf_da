from flask import render_template, url_for, flash, redirect, request, session
from tracking_tool import app, db, bcrypt
from flaskext.mysql import MySQL
from flask_login import login_user, current_user, logout_user, login_required
from tracking_tool.models import User
from tracking_tool.forms import RegistrationForm, LoginForm
from datetime import timedelta

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.authorization == 0:
                return render_template('su_home.html')
            elif user.authorization == 1:
                return render_template('admin_home.html')
            elif user.authorization == 2:
                return render_template('advisor_home.html')
            elif user.authorization == 3:
                return render_template('student_home.html')
            elif user.authorization == 4:
                return render_template('parent_home.html')
            else:
                # no access to page
                return render_template('account_inactive.html')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # tells us whether form validated
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, authorization=form.authorization.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return render_template('registration_complete.html')
    return render_template('register.html', title='Register', form=form)

@app.route('/forms')
def forms():
    if session['access'] <= 2:
        return check_session('forms.html', None)
    else:
        return render_template('restricted_message.html')


@app.route('/new_student_form')
def new_student_form():
    if session['access'] <= 2:
        return check_session('new_student_form.html', None)
    else:
        return render_template('restricted_message.html')


@app.route('/student_status_change')
def student_status_change():
    if session['access'] <= 2:
        return check_session('student_status_change.html', None)
    else:
        return render_template('restricted_message.html')


@app.route('/students')
def students():
    if session['access'] <= 2:
        con = mysql.connect()
        cur = con.cursor()
        cur.execute('SELECT * FROM admins')
        data = cur.fetchall()
        return check_session('students.html', data)
    else:
        return render_template('restricted_message.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

