from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp, InputRequired, NumberRange, Email
from ..models import User, UniversitySchool, UniversityYear
from flask_login import current_user
# from datetime import timedelta, date

class RegistrationForm(FlaskForm):
    university_year_choices = [('','Select a Year')]
    university_school_choices = [('','Select a School')]
    
    if UniversityYear.query.order_by(UniversityYear.name).first():
        university_year_choices += [(university_year.id, university_year.name) for university_year in UniversityYear.query.order_by(UniversityYear.name).all()]

    if UniversitySchool.query.order_by(UniversitySchool.name).first():
        university_school_choices += [(university_school.id, university_school.name) for university_school in UniversitySchool.query.order_by(UniversitySchool.name).all()]

    # input fields
    username = StringField('Username *', validators = [DataRequired(), Length(min = 2, max = 30)])
    firstname = StringField('First Name *', validators = [DataRequired(), Length(min = 2, max = 30)])
    lastname = StringField('Last Name *', validators = [DataRequired(), Length(min = 2, max = 100)])
    email = StringField('Email *', validators = [DataRequired(), Length(min = 2, max = 30)]) # , Email()])
    password = PasswordField('Password *', validators = [DataRequired()]) #, Regexp('^(? = .*\d).{6,8}$', message = 'Your password should be between 6 and 8 Charaters long and contain at least 1 number')])
    confirm_password = PasswordField('Confirm Password *', validators = [DataRequired(), EqualTo('password', message = 'Passwords do not match')])
    university_year = SelectField('University Year *', choices = university_year_choices, validators = [DataRequired()])
    university_school = SelectField('University School *', choices = university_school_choices, validators = [DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username already Taken. Please choose a different one.')

    def validate_email(self, email):
       email = User.query.filter_by(email = email.data.lower() + '@cardiff.ac.uk').first()
       if email:
           raise ValidationError('Email already Used. Please Use a different one.')

    def validate_university_year(self, university_year):
       if university_year == 0:
           raise ValidationError('Please select a Year')

    def validate_university_school(self, university_school):
       if university_school == 0:
           raise ValidationError('Please select a School')


class LoginForm(FlaskForm):
    username_email = StringField('Username or Email *', validators=[DataRequired()])
    password = PasswordField('Password *', validators=[DataRequired()]) # Regexp('^(?=.*\d).{6,8}$', message='Your password should be between 6 and 8 Charaters long and contain at least 1 number')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Display Name *', validators=[DataRequired(), Length(min=2, max=15)])
    # email = StringField('Email *', validators=[DataRequired(), Email()])
    firstname = StringField('First Name *', validators=[DataRequired(), Length(min=2, max=15)])
    lastname = StringField('Last Name *', validators=[DataRequired(), Length(min=2, max=15)])
    bio = TextAreaField('About yourself')
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

class AddUniversityForm(FlaskForm):
    name = StringField('University *', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Add University')

class AddUniYearForm(FlaskForm):
    name = StringField('University Year *', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Add Uni Year')


class AddUniSchoolForm(FlaskForm):
    name = StringField('University School *', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Add Uni School')

class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Old Password *', validators=[DataRequired()])
    new_password = PasswordField('New Password *', validators = [DataRequired()]) #, Regexp('^(? = .*\d).{6,8}$', message = 'Your password should be between 6 and 8 Charaters long and contain at least 1 number')])
    confirm_new_password = PasswordField('Confirm New Password *', validators = [DataRequired(), EqualTo('new_password', message = 'Passwords do not match')])
    submit = SubmitField('Change Password')
