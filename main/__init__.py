from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import timedelta
import os


""" > Move to config.py file for local development

from datetime import timedelta
secret_key = '<- add secret key here ->'
database_uri = 'mysql+pymysql://<- DB Username ->:<- DB Password ->@<- DB domain or IP (localhost normally) ->/<- DB Name ->'
# database_uri = 'mysql+pymysql://root@localhost/<- DB Name ->' # normal settings for local mySQL DB
debug_setting = True # for local deveplement server only
remember_cookie_duration = timedelta(days=1) # change duration for your own needs
sqlalchemy_track_modifications = False

"""


SECRET_KEY = ''
SQLALCHEMY_DATABASE_URI = ''
DEBUG = False
REMEMBER_COOKIE_DURATION = timedelta(days=1) # Still will result in the cookies, for a logeding user, will expire after 1 day
SQLALCHEMY_TRACK_MODIFICATIONS = False

if os.path.exists('main/config.py'):
    from .config import secret_key, database_uri, debug_setting, remember_cookie_duration, sqlalchemy_track_modifications
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = database_uri
    DEBUG = debug_setting
    REMEMBER_COOKIE_DURATION = remember_cookie_duration
    SQLALCHEMY_TRACK_MODIFICATIONS = sqlalchemy_track_modifications

app = Flask(__name__)

# Note: Environment variables override the config.py file

# secret_key_setting
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") if os.environ.get("SECRET_KEY") else SECRET_KEY

# database_setting
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI") if os.environ.get("SQLALCHEMY_DATABASE_URI") else SQLALCHEMY_DATABASE_URI

# debug_setting
app.config['DEBUG'] = os.environ.get("DEBUG") if os.environ.get("DEBUG") else DEBUG

# remember_me_cookie_setting
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days = os.environ.get("REMEMBER_COOKIE_DURATION")) if os.environ.get("REMEMBER_COOKIE_DURATION") else REMEMBER_COOKIE_DURATION

# sqlalchemy_modifications_setting
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") if os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") else SQLALCHEMY_TRACK_MODIFICATIONS

# Database setup with login featues 
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)



## Reference for blueprints: https://flask.palletsprojects.com/en/2.2.x/blueprints/
# import blueprint
from .user.routes import users
from .student.routes import students
from .module.routes import modules
from .social.routes import socials
# from .system.routes import system
from .system import routes

# register blueprint
app.register_blueprint(users)
app.register_blueprint(students)
app.register_blueprint(modules)
app.register_blueprint(socials)
# app.register_blueprint(system)

# from . import routes # This is nolonger needed as everything now uses blueprints
