from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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
REMEMBER_COOKIE_DURATION = timedelta(days=1)
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
app.config['REMEMBER_COOKIE_DURATION'] = os.environ.get("REMEMBER_COOKIE_DURATION") if os.environ.get("REMEMBER_COOKIE_DURATION") else REMEMBER_COOKIE_DURATION

# sqlalchemy_modifications_setting
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") if os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") else SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

bcrypt = Bcrypt(app)

from . import routes