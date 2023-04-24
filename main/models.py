from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin
import secrets


# many to many tables #
# """
# Links a user to one or more roles
# """
# user_role_link = db.Table(
#     'user_role_link',
#     db.Column('user', db.String(20), db.ForeignKey('user.id'), nullable = False),
#     db.Column('user_role', db.String(20), db.ForeignKey('user_role.id'), nullable = False)
# )

# """
# Links an university to one or more image
# """
# image_university_link = db.Table(
#     'image_university_link',
#     db.Column('image', db.String(20), db.ForeignKey('image.id'), nullable = False),
#     db.Column('university', db.String(20), db.ForeignKey('university.id'), nullable = False)
# )

# """
# Links an Document to one or more Message
# """
# document_user_link = db.Table(
#     'document_user_link',
#     db.Column('user', db.String(20), db.ForeignKey('user.id'), nullable = False),
#     db.Column('document', db.String(20), db.ForeignKey('document.id'), nullable = False)
# )

# """
# Links an Image to one or more Message
# """
# image_user_link = db.Table(
#     'image_user_link',
#     db.Column('user', db.String(20), db.ForeignKey('user.id'), nullable = False),
#     db.Column('image', db.String(20), db.ForeignKey('image.id'), nullable = False)
# )

"""
Links a user to one or more message_thread
"""
user_message_thread_link = db.Table(
    'user_message_thread_link',
    db.Column('user', db.String(20), db.ForeignKey('user.id'), nullable = False),
    db.Column('message_thread', db.String(20), db.ForeignKey('message_thread.id'), nullable = False)
)


""" > Example Table: 
> Resource: https://docs.sqlalchemy.org/en/14/core/type_basics.html

class Example(db.Model):
    id = db.Column(db.String(20), primary_key = True)
    int = db.Column(db.Integer, nullable = False)
    float = db.Column(db.Float, nullable = False)
    bool = db.Column(db.Boolean, nullable = False)
    text = db.Column(db.Text, nullable = True)
    date = db.Column(db.DateTime, nullable = True, default = datetime.utcnow)

    # Links (ForeignKeys) #
    foreign_id = db.Column(db.String(20), db.ForeignKey('foreign.id'), nullable = False)

    # Relationships #
    device = db.relationship('Example2', backref = 'example', lazy = True, foreign_keys = 'Example2.example_id')

"""


class User(UserMixin, db.Model):
    # Datebase Columns 
    """
    Used to define what a user object is
    """
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    username = db.Column(db.String(120), nullable = False)
    firstname = db.Column(db.String(120), nullable = True)
    lastname = db.Column(db.String(120), nullable = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    join_date = db.Column(db.DateTime, nullable = True, default = datetime.utcnow)
    is_admin = db.Column(db.Boolean, nullable = False, default = False)

    # Links (ForeignKeys) #
    university_id = db.Column(db.String(20), db.ForeignKey('university.id'), nullable = True)
    university_year_id = db.Column(db.String(20), db.ForeignKey('university_year.id'), nullable = True)
    university_school_id = db.Column(db.String(20), db.ForeignKey('university_school.id'), nullable = True)

    # Relationships #
    # user_settings = db.relationship('UserSettings', backref = 'user', lazy = True, foreign_keys = 'UserSettings.user_id')
    # user_stats = db.relationship('UserStats', backref = 'user', lazy = True, foreign_keys = 'UserStats.user_id')
    # university_review = db.relationship('UniversityReview', backref = 'user', lazy = True, foreign_keys = 'UniversityReview.user_id')
    # module_review = db.relationship('ModuleReview', backref = 'user', lazy = True, foreign_keys = 'ModuleReview.user_id')
    # module_lecture = db.relationship('ModuleLecture', backref = 'user', lazy = True, foreign_keys = 'ModuleLecture.user_id')
    # module_lectue_vote = db.relationship('ModuleLectueVote', backref = 'user', lazy = True, foreign_keys = 'ModuleLectueVote.user_id')
    module_question = db.relationship('ModuleQuestion', backref = 'user', lazy = True, foreign_keys = 'ModuleQuestion.user_id')
    module_question_comment = db.relationship('ModuleQuestionComment', backref = 'user', lazy = True, foreign_keys = 'ModuleQuestionComment.user_id')
    # module_note = db.relationship('ModuleNote', backref = 'user', lazy = True, foreign_keys = 'ModuleNote.user_id')
    module_subscription = db.relationship('ModuleSubscription', backref = 'user', lazy = True, foreign_keys = 'ModuleSubscription.user_id')
    # public_profile = db.relationship('PublicProfile', backref = 'user', lazy = True, foreign_keys = 'PublicProfile.user_id')
    public_post = db.relationship('PublicPost', backref = 'user', lazy = True, foreign_keys = 'PublicPost.user_id')
    public_post_comment = db.relationship('PublicPostComment', backref = 'user', lazy = True, foreign_keys = 'PublicPostComment.user_id')
    message_thread_owner = db.relationship('MessageThread', backref = 'user', lazy = True, foreign_keys = 'MessageThread.user_id')
    message = db.relationship('Message', backref = 'user', lazy = True, foreign_keys = 'Message.user_id')
    image = db.relationship('Image', backref = 'user', lazy = True, foreign_keys = 'Image.user_id')
    document = db.relationship('Document', backref = 'user', lazy = True, foreign_keys = 'Document.user_id')
    module_resource = db.relationship('ModuleResource', backref = 'user', lazy = True, foreign_keys = 'ModuleResource.user_id')

    # M2M Relationships #
    in_thread = db.relationship('MessageThread', backref = 'following_user', secondary = user_message_thread_link)
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class UserRole(db.Model):
    # Datebase Columns 
    """"
    Will link to a user to define what their role will be
    """
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    name = db.Column(db.String(60), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)
    user_count = db.Column(db.Integer, nullable = False, default = 0)

    # Links (ForeignKeys) #

    # Relationships #
    # Add Here
    

# class UserSettings(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
#     darkmode = db.Column(db.Boolean, nullable = False, default = False)
#     date_edited = db.Column(db.DateTime, nullable = True)

#     # Links (ForeignKeys) #
#     user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)

#     # Relationships #
#     # Add Here
    

# class UserStats(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
#     posts = db.Column(db.Integer, nullable = False, default = 0)
#     comments = db.Column(db.Integer, nullable = False, default = 0)
#     friends = db.Column(db.Integer, nullable = False, default = 0)
#     reviews = db.Column(db.Integer, nullable = False, default = 0)
#     date_edited = db.Column(db.DateTime, nullable = True)

#     # Links (ForeignKeys) #
#     user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)

#     # Relationships #
#     # Add Here
    

# University
class University(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    name = db.Column(db.String(120), nullable = False)
    url = db.Column(db.String(300), nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)
    date_established = db.Column(db.DateTime, nullable = True)
    first_line = db.Column(db.String(120), nullable = True)
    second_line = db.Column(db.String(120), nullable = True)
    city = db.Column(db.String(100), nullable = True)
    country = db.Column(db.String(100), nullable = True)
    postcode = db.Column(db.String(20), nullable = True) # Use this later to validate postcodes https://pypi.org/project/uk-postcode-utils/
    user_count = db.Column(db.Integer, nullable = False, default = 0)
    avg_rating = db.Column(db.Float, nullable = False, default = 0)
    
    # Links (ForeignKeys) #
    # logo_image_id = db.Column(db.String(20), db.ForeignKey('image.id'), nullable = True)

    # Relationships #
    # user = db.relationship('User', backref = 'university', lazy = True, foreign_keys = 'User.university_id')
     

# University
class UniversitySchool(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    name = db.Column(db.String(120), nullable = False)
    user_count = db.Column(db.Integer, nullable = False, default = 0)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)

    # Links (ForeignKeys) #

    # Relationships #
    # user = db.relationship('User', backref = 'university_school', lazy = True, foreign_keys = 'User.university_school_id')
    # module = db.relationship('Module', backref = 'university_school', lazy = True, foreign_keys = 'Module.university_school_id')
    
class UniversityYear(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    name = db.Column(db.String(120), nullable = False)
    user_count = db.Column(db.Integer, nullable = False, default = 0)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)

    # Links (ForeignKeys) #

    # Relationships #
    # user = db.relationship('User', backref = 'university_year', lazy = True, foreign_keys = 'User.university_year_id')
    # module = db.relationship('Module', backref = 'university_year', lazy = True, foreign_keys = 'Module.university_year_id')
    
# class UniversityReview(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
#     rating = db.Column(db.Integer, nullable = False, default = 0) # this will be 1-5 for the ratings
#     title = db.Column(db.String(240), nullable = True)
#     description = db.Column(db.Text, nullable = True)
#     date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     date_edited = db.Column(db.DateTime, nullable = True)

#     # Links (ForeignKeys) #
#     user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)

#     # Relationships #
#     # Add Here


# Module
class Module(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    name = db.Column(db.String(240), nullable = False)
    code = db.Column(db.String(30), nullable = False)
    avg_rating = db.Column(db.Float, nullable = False, default = 0)
    description = db.Column(db.Text, nullable = True)
    tutor = db.Column(db.String(240), nullable = True, default = "Unknown")
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)

    # Links (ForeignKeys) #
    university_id = db.Column(db.String(20), db.ForeignKey('university.id'), nullable = True)
    university_school_id = db.Column(db.String(20), db.ForeignKey('university_school.id'), nullable = True)
    university_year_id = db.Column(db.String(20), db.ForeignKey('university_year.id'), nullable = True)
    message_thread_id = db.Column(db.String(20), db.ForeignKey('message_thread.id'), nullable = True)

    # Relationships #
    module_question = db.relationship('ModuleQuestion', backref = 'module', lazy = True, foreign_keys = 'ModuleQuestion.module_id')
    # module_question_comment = db.relationship('ModuleQuestionComment', backref = 'module', lazy = True, foreign_keys = 'ModuleQuestionComment.module_id')
    # module_lecture = db.relationship('ModuleLecture', backref = 'module', lazy = True, foreign_keys = 'ModuleLecture.module_id')
    # module_lecture_vote = db.relationship('ModuleLectureVote', backref = 'module', lazy = True, foreign_keys = 'ModuleLectureVote.module_id')
    # module_note = db.relationship('ModuleNote', backref = 'module', lazy = True, foreign_keys = 'ModuleNote.module_id')
    module_resource = db.relationship('ModuleResource', backref = 'module', lazy = True, foreign_keys = 'ModuleResource.module_id')
    module_subscription = db.relationship('ModuleSubscription', backref = 'module', lazy = True, foreign_keys = 'ModuleSubscription.module_id')

class ModuleSubscription(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True) # Must be randomly generated -> default = secrets.token_hex(10)
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # nickname = db.Column(db.String(20), nullable = True)
    # order = db.Column(db.Integer, nullable = True)

    # Links (ForeignKeys)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
    module_id = db.Column(db.String(20), db.ForeignKey('module.id'), nullable = False)

    # Relationships #
    # Add Here


class ModuleReview(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    title = db.Column(db.String(240), nullable = True)
    rating = db.Column(db.Integer, nullable = False, default = 0)
    description = db.Column(db.Text, nullable = True)
    date_sent = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)


    # Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
    module_id = db.Column(db.String(20), db.ForeignKey('module.id'), nullable = False)

    # Relationships #
    # Add Here


# class ModuleLecture(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
#     date_sent = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     date_edited = db.Column(db.DateTime, nullable = True)

#     # Links (ForeignKeys) #
#     user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
#     module_id = db.Column(db.String(20), db.ForeignKey('module.id'), nullable = False)

#     # Relationships #
#     # module_lecture_vote = db.relationship('ModuleLectueVote', backref = 'module_lecture', lazy = True, foreign_keys = 'ModuleLectureVote.module_lecture_id')


# class ModuleLectueVote(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
#     date_sent = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     vote = db.Column(db.Boolean, nullable = False)

#     # Links (ForeignKeys) #
#     user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
#     module_id = db.Column(db.String(20), db.ForeignKey('module.id'), nullable = False)
#     module_lecture_id = db.Column(db.String(20), db.ForeignKey('module_lecture.id'), nullable = False)

#     # Relationships #
    

class ModuleQuestion(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    title = db.Column(db.String(240), nullable = False)
    description = db.Column(db.Text, nullable = True)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)
    solved = db.Column(db.Boolean, nullable = False, default = False)
    comment_count = db.Column(db.Integer, nullable = True, default = 0)
    view_count = db.Column(db.Integer, nullable = True, default = 0)
    unique_view_count = db.Column(db.Integer, nullable = True, default = 0)

    # Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
    module_id = db.Column(db.String(20), db.ForeignKey('module.id'), nullable = False)
    answer_comment_id = db.Column(db.String(20), db.ForeignKey('module_question_comment.id'), nullable = True)

    # Relationships #
    module_question_edit = db.relationship('ModuleQuestionEdit', backref = 'module_question', lazy = True, foreign_keys = 'ModuleQuestionEdit.module_question_id')
    module_question_comment = db.relationship('ModuleQuestionComment', backref = 'module_question', lazy = True, foreign_keys = 'ModuleQuestionComment.module_question_id')
    

class ModuleQuestionEdit(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    description = db.Column(db.Text, nullable = True)
    order = db.Column(db.Integer, nullable = True, default = 0)

    # Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
    module_question_id = db.Column(db.String(20), db.ForeignKey('module_question.id'), nullable = False)

    # Relationships #
    # Add Here
    

class ModuleQuestionComment(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    date_sent = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)
    message = db.Column(db.Text, nullable = False)
    sub_comment_count = db.Column(db.Integer, nullable = True, default = 0)

    # Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
    module_question_id = db.Column(db.String(20), db.ForeignKey('module_question.id'), nullable = False)
    parent_comment_id = db.Column(db.String(20), db.ForeignKey('module_question_comment.id'), nullable = True)

    # Relationships #
    # reference for using remote_side: https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side [accessed: 30 March 2023]
    module_question_comment = db.relationship('ModuleQuestionComment', backref = 'parent_comment', lazy = True, remote_side = id, foreign_keys = 'ModuleQuestionComment.parent_comment_id')
    # module_question = db.relationship('ModuleQuestion', backref = 'answer_comment', lazy = True, foreign_keys = 'ModuleQuestion.answer_comment_id')
    


#Module Resoure
# class ModuleNote(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
#     date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     date_edited = db.Column(db.DateTime, nullable = True)
#     title = db.Column(db.String(240), nullable = True)
#     description = db.Column(db.Text, nullable = True)

#     # Links (ForeignKeys) #
#     user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
#     module_id = db.Column(db.String(20), db.ForeignKey('module.id'), nullable = False)

#     # Relationships #
#     # Add Here
    

class ModuleResource(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    

    # Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
    module_id = db.Column(db.String(20), db.ForeignKey('module.id'), nullable = False)
    image_id = db.Column(db.String(20), db.ForeignKey('image.id'), nullable = True)
    document_id = db.Column(db.String(20), db.ForeignKey('document.id'), nullable = True)
    # url_id = db.Column(db.String(20), db.ForeignKey('u_r_l.id'), nullable = True)

    # Relationships #
    # Add Here
    

# Public/Social #
# class PublicProfile(db.Model):
#     # Datebase Columns 
#     id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
#     username = db.Column(db.String(50), nullable = False)
#     bio = db.Column(db.Text, nullable = True)
#     date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     date_edited = db.Column(db.DateTime, nullable = True)

#     # Links (ForeignKeys) #
#     user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)

#     # Relationships #
#     # Add Here
    

class PublicPost(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    title = db.Column(db.String(240), nullable = False)
    description = db.Column(db.Text, nullable = True)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)
    comment_count = db.Column(db.Integer, nullable = True, default = 0)
    view_count = db.Column(db.Integer, nullable = True, default = 0)
    unique_view_count = db.Column(db.Integer, nullable = True, default = 0)

    # Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
    university_id = db.Column(db.String(20), db.ForeignKey('university.id'), nullable = True)
    university_school_id = db.Column(db.String(20), db.ForeignKey('university_school.id'), nullable = True)
    university_year_id = db.Column(db.String(20), db.ForeignKey('university_year.id'), nullable = True)

    # Relationships #

class PublicPostComment(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)
    message = db.Column(db.Text, nullable = False)
    sub_comment_count = db.Column(db.Integer, nullable = True, default = 0)

    # Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
    public_post_id = db.Column(db.String(20), db.ForeignKey('public_post.id'), nullable = False)
    parent_comment_id = db.Column(db.String(20), db.ForeignKey('public_post_comment.id'), nullable = True)

    # Relationships #
    # reference for using remote_side: https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side [accessed: 30 March 2023]
    public_post_comment = db.relationship('PublicPostComment', backref = 'parent_comment', lazy = True, remote_side = id, foreign_keys = 'PublicPostComment.parent_comment_id')
    

class MessageThread(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    name = db.Column(db.String(240), nullable = True)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_last_message = db.Column(db.DateTime, nullable = True, default = datetime.utcnow)
    member_count = db.Column(db.Integer, nullable = False, default = 0)
    message_count = db.Column(db.Integer, nullable = False, default = 0) 
    
    # Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = True)

    # Relationships #
    message = db.relationship('Message', backref = 'thread', lazy = True, foreign_keys = 'Message.message_thread_id')
    module = db.relationship('Module', backref = 'thread', lazy = True, foreign_keys = 'Module.message_thread_id')

class Message(db.Model):
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    body = db.Column(db.Text, nullable = False)
    date_sent = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)

    # Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)
    message_thread_id = db.Column(db.String(20), db.ForeignKey('message_thread.id'), nullable = False)

    # Relationships #
    # Add Here
    

# System
class Image(db.Model):
    """
    To store image information
    """
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    title = db.Column(db.String(240), nullable = True)
    description = db.Column(db.Text, nullable = True)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    imagekit_id = db.Column(db.String(300), nullable = True)
    file_type = db.Column(db.String(20), nullable = True)


    # Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)

    # Relationships #
    # university = db.relationship('University', backref = 'image', lazy = True, foreign_keys = 'University.logo_image_id')
    module_resource = db.relationship('ModuleResource', backref = 'image', lazy = True, foreign_keys = 'ModuleResource.image_id')
    

class Document(db.Model):
    """
    To store document information
    """
    # Datebase Columns 
    id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
    title = db.Column(db.String(240), nullable = True)
    description = db.Column(db.Text, nullable = True)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    imagekit_id = db.Column(db.String(300), nullable = True)
    file_type = db.Column(db.String(20), nullable = True)


    # Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)

    # Relationships #
    module_resource = db.relationship('ModuleResource', backref = 'document', lazy = True, foreign_keys = 'ModuleResource.document_id')
    

# class URL(db.Model):
#     """
#     To store document information
#     """
#     # Datebase Columns 
#     id = db.Column(db.String(20), primary_key = True, default = secrets.token_hex(10))
#     title = db.Column(db.String(240), nullable = True)
#     description = db.Column(db.Text, nullable = True)
#     date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)


#     # Links (ForeignKeys) #
#     user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)

#     # Relationships #
#     module_resource = db.relationship('ModuleResource', backref = 'document', lazy = True, foreign_keys = 'ModuleResource.document_id')
     
    