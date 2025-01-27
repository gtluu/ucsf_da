from flask import render_template, url_for, flash, redirect, request, session
from tracking_tool import app, db, bcrypt, mail
from flaskext.mysql import MySQL
from flask_login import login_user, current_user, logout_user, login_required
from tracking_tool.models import User, Admins, Advisors, Parents, Students
from tracking_tool.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from datetime import timedelta
from flask_mail import Message

def check_session(page, data):
    try:
        if session['logged_in']:
            if data:
                return render_template(page, data=data)
            else:
                return render_template(page)
        else:
            return render_template('login.html', title='Login', form=form)
    except KeyError:
        return render_template('login.html', title='Login', form=form)

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
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # tells us whether form validated
    if form.validate_on_submit():

        # set authorization level based on user status
        is_admin = Admins.query.filter_by(id=form.ucsf_da_id.data).all()
        is_advisor = Advisors.query.filter_by(id=form.ucsf_da_id.data).all()
        is_student = Students.query.filter_by(id=form.ucsf_da_id.data).all()
        is_parent = Parents.query.filter_by(id=form.ucsf_da_id.data).all()

        if is_admin and not is_advisor and not is_student and not is_parent:
            authorization = 1
        elif is_advisor and not is_admin and not is_student and not is_parent:
            authorization = 2
        elif is_student and not is_admin and not is_advisor and not is_parent:
            authorization = 3
        elif is_parent and not is_admin and not is_advisor and not is_student:
            authorization = 4
        else:
            authorization = 5

        # create user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, authorization=authorization, ucsf_da_id=form.ucsf_da_id.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
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

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made.
'''

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        # checks whether email is associated with UCSF DA affiliated member
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm
    if form.validate_on_submit():

        # set authorization level based on user status
        is_admin = Admins.query.filter_by(id=form.ucsf_da_id.data).all()
        is_advisor = Advisors.query.filter_by(id=form.ucsf_da_id.data).all()
        is_student = Students.query.filter_by(id=form.ucsf_da_id.data).all()
        is_parent = Parents.query.filter_by(id=form.ucsf_da_id.data).all()

        if is_admin and not is_advisor and not is_student and not is_parent:
            authorization = 1
        elif is_advisor and not is_admin and not is_student and not is_parent:
            authorization = 2
        elif is_student and not is_admin and not is_advisor and not is_parent:
            authorization = 3
        elif is_parent and not is_admin and not is_advisor and not is_student:
            authorization = 4
        else:
            authorization = 5

        # create user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password= hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

