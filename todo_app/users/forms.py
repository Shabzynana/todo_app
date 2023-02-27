from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.fields.html5 import DateField, EmailField, TelField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from todo_app.models import User

class LoginForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):

    email = EmailField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    first_name = StringField('FirstName',validators=[DataRequired()])
    last_name = StringField('LastName',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(), EqualTo('pass_confirm', message = "password must match")])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    gender = RadioField('Please choose your mood:', choices=[('M','Male'),('F','Female')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message = "password must match")])
    submit = SubmitField('Reset Password')

class Change_DpForm(FlaskForm):

    picture = FileField('Pick a Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

class UpdateUserForm(FlaskForm):

    first_name = StringField('FirstName',validators=[DataRequired()])
    last_name = StringField('LastName',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
