from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin
import secrets



""" > Example Table: 
> Resource: https://docs.sqlalchemy.org/en/14/core/type_basics.html

class Example(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    int = db.Column(db.Integer, nullable=False)
    float = db.Column(db.Float, nullable=False)
    bool = db.Column(db.Boolen, nullable=False)
    text = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable = True, default = datetime.utcnow)

    # Links (ForeignKeys) #
    foreign_id = db.Column(db.String(20), db.ForeignKey('foreign.id'), nullable = False)

    # Relationships #
    device = db.relationship('Example', backref = 'example', lazy = True, foreign_keys = 'Example2.example2_id')

"""


class User(UserMixin, db.Model):
    id = db.Column(db.String(20), primary_key=True, default = secrets.token_hex(10))
    username = db.Column(db.String(120), nullable=False)
    firstname = db.Column(db.String(120), nullable=True)
    lastname = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    join_date = db.Column(db.DateTime, nullable = True, default = datetime.utcnow)

    # Links (ForeignKeys) #
    # - Nothing Here -
    # Example: role_id = db.Column(db.String(20), db.ForeignKey('role.id'), nullable = False)

    # Relationships #
    # - Nothing Here -
    # Example: order = db.relationship('Order', backref = 'user', lazy = True, foreign_keys = 'Order.user_id')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


class UserRole(db.Model):
    pass

class Friends(db.Model):
    pass

class UserProfile(db.Model):
    pass

class UserSettings(db.Model):
    pass

class UserStats(db.Model):
    pass


# University
class University(db.Model):
    pass

class UniversityRating(db.Model):
    pass

class UniversitySchool(db.Model):
    pass

class UniversityYear(db.Model):
    pass


# Module
class Module(db.Model):
    pass

class ModuleRating(db.Model):
    pass

class ModuleLecture(db.Model):
    pass

class ModuleLectueVote(db.Model):
    pass

class ModulePost(db.Model):
    pass

class ModulePostComment(db.Model):
    pass


#Module Resoure
class ModuleNote(db.Model):
    pass

class ModuleFile(db.Model):
    pass


# Public
class PublicProfile(db.Model):
    pass

class PublicPost(db.Model):
    pass

class PublicPostComment(db.Model):
    pass

class MessageGroup(db.Model):
    pass

class Message(db.Model):
    pass


# System
class Image(db.Model):
    pass

class Document(db.Model):
    pass