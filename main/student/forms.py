from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp, InputRequired, NumberRange
from ..models import ModuleSubscription, Module
from flask_login import current_user
from ..main_utils import aside_dict

class CreateNoteForm(FlaskForm):
    title = StringField('Title*', validators = [DataRequired(), Length(max = 50)], description="The title for the note", render_kw={'placeholder':"Title*"})
    text = TextAreaField('Note', validators = [Length(max = 10000)], description="This is where you write your amazing note", render_kw={'placeholder':"This is where you write your amazing note"})

    submit = SubmitField('Save')