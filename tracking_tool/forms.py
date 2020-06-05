from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tracking_tool.models import *


class RegistrationForm(FlaskForm):
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
                                            ('Bullworth Academy', 'Bullworth Academy')])
    submit = SubmitField('Filter')
