from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tracking_tool.models import *
import configparser
import os


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    ucsf_da_id = IntegerField("Enter UCSF Doctor's Academy ID", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create New User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        # if user already exists
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_ucsf_da_id(self, ucsf_da_id):
        user = User.query.filter_by(ucsf_da_id=ucsf_da_id.data).first()

        # if ucsf_da_id already exists
        if user:
            raise ValidationError('Invalid ID.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class FilterSortStudents(FlaskForm):
    student_id = StringField('Student ID')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    school = SelectField('school', choices=[('All', 'All'),
                                            ('Shujin Academy', 'Shujin Academy'),
                                            ('Blackwell Academy', 'Blackwell Academy'),
                                            ('Bullworth Academy', 'Bullworth Academy')])
    grade = SelectField('Grade', choices=[('All', 'All'),
                                          ('Freshman', 'Freshman'),
                                          ('Sophomore', 'Sophomore'),
                                          ('Junior', 'Junior'),
                                          ('Senior', 'Senior')])
    min_exp_grad = StringField('Expected Graduation')
    max_exp_grad = StringField('Expected Graduation')
    min_gpa = StringField('GPA')
    max_gpa = StringField('GPA')
    status = SelectField('Student Status', choices=[('All', 'All'),
                                                    ('Good Standing', 'Good Standing'),
                                                    ('Intervention', 'Intervention'),
                                                    ('Probation', 'Probation'),
                                                    ('Excused', 'Excused'),
                                                    ('Withdrawn', 'Withdrawn'),
                                                    ('Moved', 'Moved')])
    fmp_id = StringField('FMP ID')
    parent_id = StringField('Parent ID')
    advisor_id = StringField('Advisor ID')
    submit = SubmitField('Filter')


class FilterSortAdvisors(FlaskForm):
    advisor_id = StringField('Advisor ID')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    school = SelectField('school', choices=[('All', 'All'),
                                            ('Shujin Academy', 'Shujin Academy'),
                                            ('Blackwell Academy', 'Blackwell Academy'),
                                            ('Bullworth Academy', 'Bullworth Academy')], default='All')
    submit = SubmitField('Filter')


class StudentStatusChange(FlaskForm):
    student_id = StringField('Student ID')
    status = SelectField('Student Status', choices=[('Good Standing', 'Good Standing'),
                                                    ('Intervention', 'Intervention'),
                                                    ('Probation', 'Probation'),
                                                    ('Excused', 'Excused'),
                                                    ('Withdrawn', 'Withdrawn'),
                                                    ('Moved', 'Moved')])
    config = configparser.ConfigParser()
    config.read(os.path.dirname(__file__) + '/static/txt/student_status_form.txt')
    checkbox1 = BooleanField(config['checkbox1']['txt'])
    field1 = TextAreaField(config['field1']['txt'])
    checkbox2 = BooleanField(config['checkbox2']['txt'])
    field2 = TextAreaField('Student Goals')
    checkbox3 = BooleanField(config['checkbox3']['txt'])
    field3 = TextAreaField('')
    field4 = TextAreaField('Additional Notes')
    submit = SubmitField('Submit')


class SignatureForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign')


class ProgramInterventionPlanForm(FlaskForm):
    status = BooleanField('Intervention')
    field1 = TextAreaField('Reason for Program Intervention')
    field2 = TextAreaField('What is the plan for intervention?')
    field3 = TextAreaField('How will student successfully exit the intervention?')
    submit = SubmitField('Submit')


class ProbationForm(FlaskForm):
    status = BooleanField('Probation')
    field1 = TextAreaField('Reason for Program Probation')
    field2 = TextAreaField('How will student successfully exit probation?')
    submit = SubmitField('Submit')


class WithdrawalForm(FlaskForm):
    status = BooleanField('Withdrawn')
    type = SelectField('Type of Withdrawal', choices=[('Voluntary', 'Voluntary'),
                                                      ('Academic Dismissal', 'Academic Dismissal'),
                                                      ('Other', 'Other')])
    field1 = TextAreaField('Reason for Withdrawal')
    checkbox1 = BooleanField('Student was provided with reinstatement policy.')
    checkbox2 = BooleanField('Meeting was held with student and parent/guardian.')
    checkbox3 = BooleanField('Student is provided with Exit Survey link.')
    submit = SubmitField('Submit')
