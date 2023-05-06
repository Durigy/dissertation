from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectField, URLField, FileField, DateTimeField
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


class AddModuleLectureForm(FlaskForm):
    '''
    this is a form to add a module lecture
    '''
    
    title = StringField('Title of the Lecture: *', render_kw = {"placeholder": "Give your Lecture a Title for students"}, validators = [DataRequired(), Length(min=4, max=240)])
    date_start = DateTimeField('When the lecture starts *', format='%Y-%m-%dT%H:%M')
    date_end = DateTimeField('When the lecture finishes *', format='%Y-%m-%dT%H:%M')
    location = TextAreaField('Location or Online *:', render_kw = {"placeholder": "Location of the lecture or \'Online\' if it is online"}, validators = [DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('More Detail:', render_kw = {"placeholder": "More detail about the lecture i.e what it will be about"})
    online_link = URLField('Online link i.e Zoom/Teams:', render_kw = {"placeholder": "Online link i.e Zoom/Teams"}, validators = [Length(max=300)])
    quizing_link = URLField('Quiz link i.e Mentimeter/Kahoot:', render_kw = {"placeholder": "Quiz link i.e Mentimeter/Kahoot"}, validators = [Length(max=300)])
    submit = SubmitField('Add Lecture')

    def validate_date_start(self, date_start):
       if not date_start.data:
           raise ValidationError('Please add a date')

    def validate_date_end(self, date_end):
       if not date_end.data:
           raise ValidationError('Please add a date')
       
       if date_end.data < self.date_start.data:
           raise ValidationError('A lecture can\'t end before it has started')
       
       if date_end.data == self.date_start.data:
           raise ValidationError('A lecture can\'t end and start at the same time silly')
       
       if date_end.data < datetime.now():
           raise ValidationError('If only we could go back in time, then you could set the end of a lecture to before the current time')