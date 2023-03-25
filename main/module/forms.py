from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp, InputRequired, NumberRange, Email
from ..models import University, UniversitySchool, UniversityYear
from datetime import date, datetime, time, timedelta

class AddModuleForm(FlaskForm):
    '''
    this is a form for adding modules to the the database for testing
    '''

    name = StringField('Module Name: *', render_kw={"placeholder": "Module Name"}, validators = [DataRequired(), Length(min=4, max=240)])
    code = StringField('Module Code: *', render_kw={"placeholder": "Module Code"}, validators = [DataRequired(), Length(min=4, max=30)])
    description = TextAreaField('Module Description:', render_kw={"placeholder": "Module Description"})
    submit = SubmitField('Add Module')