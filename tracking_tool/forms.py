from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tracking_tool.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    ucsf_da_id = IntegerField("Enter UCSF Doctor's Academy ID", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create New User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        # if username already exists
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
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):

        # checks whether email is associated with UCSF DA affiliated member
        admin = Admins.query.filter_by(email=email.data).first()
        advisor = Advisors.query.filter_by(email=email.data).first()
        parent = Parents.query.filter_by(email=email.data).first()
        student = Students.query.filter_by(email=email.data).first()

        # checks whether UCSF DA affiliated member's ucsf_da_id is in user db
        admin_user = User.query.filter_by(ucsf_da_id=admin.ucsf_da_id)
        advisor_user = User.query.filter_by(ucsf_da_id=advisor.ucsf_da_id)
        parent_user = User.query.filter_by(ucsf_da_id=parent.ucsf_da_id)
        student_user = User.query.filter_by(ucsf_da_id=student.ucsf_da_id)

        if admin_user is None and advisor_user is None and parent_user is None and student_user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

