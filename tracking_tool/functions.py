from flask import render_template, url_for, flash, redirect, request, session
from tracking_tool import app, db, bcrypt, mail
from flaskext.mysql import MySQL
from flask_login import login_user, current_user, logout_user, login_required
from tracking_tool.models import *
from tracking_tool.forms import RegistrationForm, LoginForm
from datetime import timedelta
import random
import string
import datetime
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


def generate_sys_id():
    id_list = [i.id for i in User.query.all()]
    while True:
        id = random.randint(10000000, 99999999)
        if id not in id_list:
            break
    return id


def set_auth_level(form):
    admin_id_list = [i.id for i in Admins.query.all()]
    advisor_id_list = [i.id for i in Advisors.query.all()]
    student_id_list = [i.id for i in Students.query.all()]
    parent_id_list = [i.id for i in Parents.query.all()]

    is_admin = int(form.ucsf_da_id.data) in admin_id_list
    is_advisor = int(form.ucsf_da_id.data) in advisor_id_list
    is_student = int(form.ucsf_da_id.data) in student_id_list
    is_parent = int(form.ucsf_da_id.data) in parent_id_list

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
    return auth


def hash_password(form):
    salt = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(128))
    return (salt, bcrypt.generate_password_hash(form.password.data + salt).decode('utf-8'))


def get_timestamp():
    timestamp = datetime.datetime.now()
    timestamp = str(timestamp.year) + '-' + str(timestamp.month) + '-' + str(timestamp.day) + ' ' +\
                str(timestamp.hour) + ':' + str(timestamp.minute) + ':' + str(timestamp.second)
    return timestamp

def find_user_in_db(form):

    # checks where email is associated with UCSF DA affiliated member
    is_admin = Admins.query.filter_by(email=form.email.data).first()
    is_advisor = Advisors.query.filter_by(email=form.email.data).first()
    is_parent = Parents.query.filter_by(email=form.email.data).first()
    is_student = Students.query.filter_by(email=form.email.data).first()

    # find user in database
    if is_admin and not is_advisor and not is_student and not is_parent:
        user = User.query.filter_by(ucsf_da_id=is_admin.id).first()
    elif is_advisor and not is_admin and not is_student and not is_parent:
        user = User.query.filter_by(ucsf_da_id=is_advisor.id).first()
    elif is_student and not is_admin and not is_student and not is_parent:
        user = User.query.filter_by(ucsf_da_id=is_student.id).first()
    elif is_parent and not is_admin and not is_advisor and not is_student:
        user = User.query.filter_by(ucsf_da_id=is_parent.id).first()
    else:
        user = None
    return user

def send_reset_email(user):

    # find which db the user is in:
    is_admin = Admins.query.filter_by(id=user.ucsf_da_id).first()
    is_advisor = Advisors.query.filter_by(id=user.ucsf_da_id).first()
    is_parent = Parents.query.filter_by(id=user.ucsf_da_id).first()
    is_student = Students.query.filter_by(id=user.ucsf_da_id).first()

    # set user variable to db entry that the user is in:
    if is_admin:
        user = is_admin
    elif is_advisor:
        user = is_advisor
    elif is_parent:
        user = is_parent
    elif is_student:
        user = is_student
    else:
        user = None

    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='sarah.woldemariam@ucsf.edu', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request, then simply ignore this email and no changes will be made.
'''
    # uncomment once we can connect to email server
    #mail.send(msg)

def client_db_that_the_token_is_in(token):

    # get token from pertinent db
    is_admin = Admins.verify_reset_token(token)
    is_advisor = Advisors.verify_reset_token(token)
    is_parent = Parents.verify_reset_token(token)
    is_student = Students.verify_reset_token(token)

    # set user to whichever variable is not None:
    if is_admin:
        user = is_admin
    elif is_advisor:
        user = is_advisor
    elif is_parent:
        user = is_parent
    elif is_student:
        user = is_student
    else:
        user = None

    return user






