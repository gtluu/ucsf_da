from flask import render_template, url_for, flash, redirect, request, session
from tracking_tool import app, db, bcrypt
from flaskext.mysql import MySQL
from flask_login import login_user, current_user, logout_user, login_required
from tracking_tool.models import *
from tracking_tool.forms import RegistrationForm, LoginForm
from datetime import timedelta
import random
import string
import datetime


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
