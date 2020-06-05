from flask import render_template, url_for, flash, redirect, request, session
from tracking_tool import app, db, bcrypt
from flaskext.mysql import MySQL
from flask_login import login_user, current_user, logout_user, login_required
from tracking_tool.functions import *
from tracking_tool.models import *
from tracking_tool.forms import *
from datetime import timedelta
import random


@app.route("/")
def root():
    return render_template('login.html', title='Login', form=LoginForm(), user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data + user.salt):
            print('logged_in')
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=LoginForm(), user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm(request.form)
    # tells us whether form validated
    if request.method == 'POST' and form.validate():
        salt, hashed_password = hash_password(form)
        user = User(id=generate_sys_id(),
                    authorization=set_auth_level(form),
                    username=form.username.data,
                    salt=salt,
                    ucsf_da_id=form.ucsf_da_id.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, user=current_user)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title='Home', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/students')
def students():
    if current_user.is_authenticated and current_user.authorization <= 2:
        form = FilterSortStudents(request.form)
        students = Students.query.all()
        return render_template('students.html', title='Students', students=students, user=current_user, form=form)
    else:
        return render_template('restricted_message.html')


@app.route('/student_filter', methods=['GET', 'POST'])
def student_filter():
    if current_user.is_authenticated and current_user.authorization <= 2:
        form = FilterSortStudents(request.form)
        if request.method == 'POST' and form.validate():
            filters = {'student_id': form.student_id.data,
                       'first_name': form.first_name.data,
                       'last_name': form.last_name.data,
                       'school': form.school.data,
                       'grade': form.grade.data,
                       'program_status': form.status.data,
                       'fmp_id': form.fmp_id.data,
                       'parent_id': form.parent_id.data,
                       'advisor_id': form.advisor_id.data}
            ranges = {'min_expected_grad': form.min_exp_grad.data,
                      'max_expected_grad': form.max_exp_grad.data,
                      'min_gpa': form.min_gpa.data,
                      'max_gpa': form.max_gpa.data}
            final_filters = {}
            for key, value in filters.items():
                if value != '' and value != 'All':
                    final_filters[key] = value
            students = Students.query.filter_by(**final_filters).all()
            if ranges['min_expected_grad'] != '' and ranges['max_expected_grad'] != '':
                if float(ranges['min_expected_grad']) <= float(ranges['max_expected_grad']):
                    students = [i for i in students
                                if float(ranges['min_expected_grad']) <= float(i.expected_grad) <=
                                float(ranges['max_expected_grad'])]
            if ranges['min_gpa'] != '' and ranges['max_gpa'] != '':
                if float(ranges['min_gpa']) <= float(ranges['max_gpa']):
                    students = [i for i in students
                                if float(ranges['min_gpa']) <= float(i.gpa) <= float(ranges['max_gpa'])]
            return render_template('students.html', title='Students', students=students, user=current_user, form=form)
    students = Students.query.all()
    flash(f'Error with filter.', 'danger')
    return render_template('students.html', title='Students', students=students, user=current_user, form=form)


@app.route('/advisors')
def advisors():
    if current_user.is_authenticated and current_user.authorization <= 2:
        form = FilterSortStudents(request.form)
        advisors = Students.query.all()
        return render_template('advisors.html', title='Advisors', advisors=advisors, user=current_user, form=form)
    else:
        return render_template('restricted_message.html')


@app.route('/new_student_form')
def new_student_form():
    if current_user.is_authenticated and current_user.authorization <= 2:
        return check_session('new_student_form.html', None)
    else:
        return render_template('restricted_message.html')


@app.route('/student_status_change')
def student_status_change():
    if current_user.is_authenticated and current_user.authorization <= 2:
        return check_session('student_status_change.html', None)
    else:
        return render_template('restricted_message.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


