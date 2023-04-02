from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp, InputRequired, NumberRange
from datetime import date, datetime, time, timedelta


class AddPostForm(FlaskForm):
    '''
    this is a form for creating a post
    '''
    
    title = StringField('Title of Post: *', render_kw = {"placeholder": "Give your Post a Title"}, validators = [DataRequired(), Length(min=4, max=240)])
    description = TextAreaField('More Detail:', render_kw = {"placeholder": "More detail about your post"})
    submit = SubmitField('Post')

class AddPublicPostCommentForm(FlaskForm):
    '''
    this is a form create a comment on a Public Post
    '''
    
    message = TextAreaField('Comment:', render_kw = {"placeholder": "Write your comment here"}, validators = [Length(min=4, max=240)])
    submit = SubmitField('Post Comment')
