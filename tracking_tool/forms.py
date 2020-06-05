from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tracking_tool.models import User


class RegistrationForm(FlaskForm):
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
