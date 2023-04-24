from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectField, URLField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp, InputRequired, NumberRange, Email
from ..models import University, UniversitySchool, UniversityYear
from datetime import date, datetime, time, timedelta
from .. import ALLOWED_EXTENSIONS

allowed_extensions = ', '.join(ALLOWED_EXTENSIONS)

class AddModuleForm(FlaskForm):
    '''
    this is a form for adding modules to the the database for testing
    '''

    university_year_choices = [('','Select a Year')]
    university_school_choices = [('','Select a School')]
    
    if UniversityYear.query.order_by(UniversityYear.name).first():
        university_year_choices += [(university_year.id, university_year.name) for university_year in UniversityYear.query.order_by(UniversityYear.name).all()]

    if UniversitySchool.query.order_by(UniversitySchool.name).first():
        university_school_choices += [(university_school.id, university_school.name) for university_school in UniversitySchool.query.order_by(UniversitySchool.name).all()]


    name = StringField('Module Name: *', render_kw = {"placeholder": "Module Name"}, validators = [DataRequired(), Length(min=4, max=240)])
    code = StringField('Module Code: *', render_kw = {"placeholder": "Module Code"}, validators = [DataRequired(), Length(min=4, max=30)])
    description = TextAreaField('Module Description:', render_kw = {"placeholder": "Module Description"})
    university_year = SelectField('University Year *', choices = university_year_choices, validators = [DataRequired()])
    university_school = SelectField('University School *', choices = university_school_choices, validators = [DataRequired()])
    submit = SubmitField('Add Module')

    def validate_university_year(self, university_year):
       if university_year == 0:
           raise ValidationError('Please select a Year')

    def validate_university_school(self, university_school):
       if university_school == 0:
           raise ValidationError('Please select a School')


class AddModuleQuestionForm(FlaskForm):
    '''
    this is a form to post a module question
    '''
    
    title = StringField('Title of Question: *', render_kw = {"placeholder": "Give your Question a Title"}, validators = [DataRequired(), Length(min=4, max=240)])
    description = TextAreaField('More Detail:', render_kw = {"placeholder": "More detail about your question"})
    submit = SubmitField('Post Question')

class AddModuleQuestionCommentForm(FlaskForm):
    '''
    this is a form is to post a comment on a module question
    '''
    
    message = TextAreaField('Comment:', render_kw = {"placeholder": "Write your comment/answer here"}, validators = [Length(min=4, max=240)])
    submit = SubmitField('Post Comment')

class AddModuleResourceForm(FlaskForm):
    '''
    this is a form is to post a comment on a module question
    '''
    
    title = StringField('Title of Resource: *', render_kw = {"placeholder": "Give your Resource a Title"}, validators = [DataRequired(), Length(min=4, max=240)])
    description = TextAreaField('More Detail:', render_kw = {"placeholder": "More detail about your resource"})
    url = URLField('Add a URL', render_kw={"placeholder": "https://www.example.com"})
    file = FileField(f'Upload a file: {allowed_extensions}', render_kw={"placeholder": f"Upload a file: {allowed_extensions}"}) #, "multiple": ""})
    submit = SubmitField('Post Resource')
