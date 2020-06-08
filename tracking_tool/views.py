from flask import render_template, url_for, flash, redirect, request, session
from tracking_tool import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from tracking_tool.functions import *
from tracking_tool.models import *
from tracking_tool.forms import *


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
        username = current_user.username
        user = User.query.filter(User.username == username).first()
        if int(user.authorization) == 1:
            user = Admins.query.filter(Admins.id == user.ucsf_da_id).first()
        elif int(user.authorization) == 2:
            user = Advisors.query.filter(Advisors.id == user.ucsf_da_id).first()
        elif int(user.authorization) == 3:
            user = Students.query.filter(Students.id == user.ucsf_da_id).first()
        elif int(user.authorization) == 4:
            user = Parents.query.filter(Parents.id == user.ucsf_da_id).first()
        return render_template('home.html', title='Home', user=current_user, user_info=user)
    else:
        return redirect(url_for('login'))


@app.route('/students')
def students():
    if current_user.is_authenticated and int(current_user.authorization) <= 2:
        form = FilterSortStudents(request.form)
        students = Students.query.all()
        return render_template('students.html', title='Students', students=students, user=current_user, form=form)
    else:
        return redirect(url_for('login'))


@app.route('/student_filter', methods=['GET', 'POST'])
def student_filter():
    form = FilterSortStudents(request.form)
    if current_user.is_authenticated and int(current_user.authorization) <= 2:
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
        form = FilterSortAdvisors(request.form)
        advisors = Advisors.query.all()
        return render_template('advisors.html', title='Advisors', advisors=advisors, user=current_user, form=form)
    else:
        return redirect(url_for('login'))


@app.route('/advisor_filter', methods=['GET', 'POST'])
def advisor_filter():
    form = FilterSortAdvisors(request.form)
    if current_user.is_authenticated and int(current_user.authorization) <= 2:
        if request.method == 'POST' and form.validate():
            filters = {'advisor_id': form.advisor_id.data,
                       'first_name': form.first_name.data,
                       'last_name': form.last_name.data,
                       'school': form.school.data}
            final_filters = {}
            for key, value in filters.items():
                if value != '' and value != 'All':
                    final_filters[key] = value
            advisors = Advisors.query.filter_by(**final_filters).all()
            return render_template('advisors.html', title='Advisors', advisors=advisors, user=current_user, form=form)
    advisors = Advisors.query.all()
    flash(f'Error with filter.', 'danger')
    return render_template('advisors.html', title='Advisors', advisors=advisors, user=current_user, form=form)


@app.route('/new_student_form')
def new_student_form():
    if current_user.is_authenticated and current_user.authorization <= 2:
        return check_session('new_student_form.html', None)
    else:
        return redirect(url_for('login'))


@app.route('/student_status_change')
def student_status_change():
    if current_user.is_authenticated and int(current_user.authorization) <= 2:
        form = StudentStatusChange(request.form)
        return render_template('student_status_change.html', title='Student Status Change Form', user=current_user,
                               form=form)
    else:
        return redirect(url_for('login'))


@app.route('/student_status_change_submit', methods=['GET', 'POST'])
def student_status_change_submit():
    form = StudentStatusChange(request.form)
    if current_user.is_authenticated and int(current_user.authorization) <= 2:
        if request.method == 'POST' and form.validate():
            gpa = Students.query.filter_by(id=form.student_id.data).first().gpa
            submitter_id = User.query.filter_by(username=current_user.username).first().ucsf_da_id
            report = Reports(id=form.student_id.data,
                             submitter_id=submitter_id,
                             timestamp=datetime.datetime.now(),
                             program_status=form.status.data,
                             gpa=gpa,
                             student_sig=0,
                             parent_sig=0,
                             intervention=form.checkbox1.data,
                             commitment=form.field1.data,
                             plan=form.checkbox2.data,
                             student_goals=form.field2.data,
                             arrange=form.checkbox3.data,
                             arrange_notes=form.field3.data,
                             additional_notes=form.field4.data)
            db.session.add(report)
            db.session.commit()
            flash(f'Student Status Change Submitted', 'success')
            return redirect(url_for('student_status_change'))
        return render_template('student_status_change.html', title='Student Status Change Form', user=current_user,
                               form=form)


@app.route('/student_report', methods=['GET', 'POST'])
def student_report():
    student_id = int(request.args.get('id'))
    student = Students.query.filter_by(id=student_id).first()
    reports = Reports.query.filter_by(id=student.id).all()
    title = student.first_name + ' ' + student.last_name
    return render_template('student_report.html', title=title, student=student, reports=reports, user=current_user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


