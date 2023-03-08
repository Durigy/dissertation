from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin
import secrets

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
# foreign_id = db.Column(db.String(20), db.ForeignKey('foreign.id'), nullable = False)

# Relationships #
    device = db.relationship('Example', backref = 'example', lazy = True, foreign_keys = 'Example2.example2_id')

"""
