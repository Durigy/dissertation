from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp, InputRequired, NumberRange, Email
from ..models import University, UniversitySchool, UniversityYear
from datetime import date, datetime, time, timedelta

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
    
    message = TextAreaField('Comment:', render_kw = {"placeholder": "Comment"}, validators = [Length(min=4, max=240)])
    submit = SubmitField('Post Comment')
