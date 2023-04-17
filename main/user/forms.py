from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp, InputRequired, NumberRange, Email
from ..models import User
from flask_login import current_user
from datetime import timedelta, date

class RegistrationForm(FlaskForm):
    username = StringField('Username *', validators=[DataRequired(), Length(min=2, max=15)])
    firstname = StringField('First Name *', validators=[DataRequired(), Length(min=2, max=15)])
    lastname = StringField('Last Name *', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email *', validators=[DataRequired(), Email()])
    password = PasswordField('Password *', validators=[DataRequired()]) #, Regexp('^(?=.*\d).{6,8}$', message='Your password should be between 6 and 8 Charaters long and contain at least 1 number')])
    confirm_password = PasswordField('Confirm Password *', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Display Name already Taken. Please choose a different one.')

    def validate_email(self, email):
       """
       TODO: add verification for uni email
       """
       email = User.query.filter_by(email=email.data).first()
       if email:
           raise ValidationError('Email already Used. Please Use a different one.')


class LoginForm(FlaskForm):
    username_email = StringField('Username or Email')
    password = PasswordField('Password', validators=[DataRequired()]) # Regexp('^(?=.*\d).{6,8}$', message='Your password should be between 6 and 8 Charaters long and contain at least 1 number')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Display Name *', validators=[DataRequired(), Length(min=2, max=15)])
    # email = StringField('Email *', validators=[DataRequired(), Email()])
    firstname = StringField('First Name *', validators=[DataRequired(), Length(min=2, max=15)])
    lastname = StringField('Last Name *', validators=[DataRequired(), Length(min=2, max=15)])
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        if username.data.lower() != current_user.username.lower():
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Display Name already Taken. Please choose a different one.')

    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         email = User.query.filter_by(email=email.data).first()
    #         if email:
    #             raise ValidationError('Email already Used. Please Use a different one.')