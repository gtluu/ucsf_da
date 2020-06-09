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
        if int(current_user.authorization) == 2:
            advisor = Advisors.query.filter_by(id=current_user.ucsf_da_id).first()
            students = Students.query.filter_by(school=advisor.school)
        else:
            students = Students.query.all()
        return render_template('students.html', title='Students', students=students, user=current_user, form=form)
    else:
        return redirect(url_for('login'))


@app.route('/student_filter', methods=['GET', 'POST'])
def student_filter():
    form = FilterSortStudents(request.form)
    if current_user.is_authenticated and int(current_user.authorization) <= 2:
        if int(current_user.authorization) == 2:
            advisor = Advisors.query.filter_by(id=current_user.ucsf_da_id).first()
            form.school.data = advisor.school
        if request.method == 'POST' and form.validate():
            filters = {'id': form.student_id.data,
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
        else:
            if int(current_user.authorization) == 2:
                advisor = Advisors.query.filter_by(id=current_user.ucsf_da_id).first()
                students = Students.query.filter_by(school=advisor.school)
            else:
                students = Students.query.all()
            flash(f'Error with filter.', 'danger')
            return render_template('students.html', title='Students', students=students, user=current_user, form=form)
    else:
        return redirect(url_for('login'))


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
            filters = {'id': form.advisor_id.data,
                       'first_name': form.first_name.data,
                       'last_name': form.last_name.data,
                       'school': form.school.data}
            final_filters = {}
            for key, value in filters.items():
                if value != '' and value != 'All':
                    final_filters[key] = value
            advisors = Advisors.query.filter_by(**final_filters).all()
            return render_template('advisors.html', title='Advisors', advisors=advisors, user=current_user, form=form)
        else:
            advisors = Advisors.query.all()
            flash(f'Error with filter.', 'danger')
            return render_template('advisors.html', title='Advisors', advisors=advisors, user=current_user, form=form)
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
            report_id_list = [i.report_id for i in Reports.query.all()]
            report_id = random.randint(1000000, 9999999)
            while report_id in report_id_list:
                report_id = random.randint(1000000, 9999999)
            report = Reports(report_id=report_id,
                             id=form.student_id.data,
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
            student = Students.query.filter_by(id=form.student_id.data).first()
            student.program_status = form.status.data
            db.session.commit()
            flash(f'Student Status Change Submitted', 'success')
            return redirect(url_for('student_status_change'))
        return render_template('student_status_change.html', title='Student Status Change Form', user=current_user,
                               form=form)
    else:
        return redirect(url_for('login'))


@app.route('/student_report', methods=['GET', 'POST'])
def student_report():
    if current_user.is_authenticated:
        if int(current_user.authorization) <= 2:
            student_id = int(request.args.get('id'))
        elif int(current_user.authorization) >= 3:
            student_id = int(request.args.get('id'))
            if student_id != current_user.ucsf_da_id:
                if int(current_user.authorization) == 3:
                    student_id = int(current_user.ucsf_da_id)
                elif int(current_user.authorization) == 4:
                    student_id = int(current_user.ucsf_da_id[:-2])
        student = Students.query.filter_by(id=student_id).first()
        tmp_reports = Reports.query.filter_by(id=student_id).all()
        reports = []
        for i in tmp_reports:
            if int(i.student_sig) != 0:
                name = student.first_name + ' ' + student.middle_name + ' ' + student.last_name
                i.student_sig = name
            if int(i.parent_sig) != 0:
                parent = Parents.query.filter_by(id=i.parent_sig).first()
                name = parent.first_name + ' ' + parent.middle_name + ' ' + parent.last_name
                i.parent_sig = name
            reports.append(i)
        title = student.first_name + ' ' + student.last_name
        return render_template('student_report.html', title=title, student=student, reports=reports, user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/report_details', methods=['GET', 'POST'])
def report_details():
    pass


@app.route('/get_signature', methods=['GET', 'POST'])
def get_signature():
    if current_user.is_authenticated:
        form_id = request.args.get('id')
        form_timestamp = request.args.get('timestamp')
        form = SignatureForm(request.form)
        return render_template('signature.html', title='Signature', form=form, form_id=form_id,
                               form_timestamp=form_timestamp, user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/sign_report', methods=['GET', 'POST'])
def sign_report():
    form = SignatureForm(request.form)
    if current_user.is_authenticated:
        if request.method == 'POST' and form.validate():
            form_id = request.args.get('form_id')
            form_timestamp = request.args.get('form_timestamp')
            report = Reports.query.filter_by(id=form_id, timestamp=form_timestamp).first()
            if int(current_user.authorization) == 3:
                signer = Students.query.filter_by(id=form_id).first()
            elif int(current_user.authorization) == 4:
                signer = Parents.query.filter_by(id=form_id).first()
            user = User.query.filter_by(ucsf_da_id=signer.id).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data + user.salt):
                if int(current_user.authorization) == 3:
                    report.student_sig = signer.id
                elif int(current_user.authorization) == 4:
                    report.student_sig = signer.id
                db.session.commit()
                return redirect(url_for('student_report', id=current_user.ucsf_da_id))
            else:
                flash(f'Incorrect Password', 'danger')
                return redirect(url_for('student_report', id=current_user.ucsf_da_id))
        else:
            flash(f'Incorrect Password', 'danger')
            return redirect(url_for('student_report', id=current_user.ucsf_da_id))
    else:
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


