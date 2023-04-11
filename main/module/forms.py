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

    name = StringField('Module Name: *', render_kw = {"placeholder": "Module Name"}, validators = [DataRequired(), Length(min=4, max=240)])
    code = StringField('Module Code: *', render_kw = {"placeholder": "Module Code"}, validators = [DataRequired(), Length(min=4, max=30)])
    description = TextAreaField('Module Description:', render_kw = {"placeholder": "Module Description"})
    submit = SubmitField('Add Module')

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
