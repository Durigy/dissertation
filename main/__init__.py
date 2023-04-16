from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_socketio import SocketIO
import os


""" > Move to config.py file for local development

from datetime import timedelta
secret_key = '<- add secret key here ->'
database_uri = 'mysql+pymysql://<- DB Username ->:<- DB Password ->@<- DB domain or IP (localhost normally) ->/<- DB Name ->'
# database_uri = 'mysql+pymysql://root@localhost/<- DB Name ->' # normal settings for local mySQL DB
debug_setting = True # for local deveplement server only
remember_cookie_duration = timedelta(days=1) # change duration for your own needs
sqlalchemy_track_modifications = False
upload_folder = '/path/to/the/uploads'
allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

"""


SECRET_KEY = ''
SQLALCHEMY_DATABASE_URI = ''
DEBUG = False
REMEMBER_COOKIE_DURATION = timedelta(days=1) # Still will result in the cookies, for a logeding user, will expire after 1 day
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = '' #{'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
IMAGE_EXTENSIONS = ''
DOCUMENT_EXTENSIONS = ''
MAX_CONTENT_LENGTH = ''

# image kit
IMAGEKIT_PRIVATE_KEY = ''
IMAGEKIT_PUBLIC_KEY = ''
IMAGEKIT_URL_ENDPOINT = ''


# from .config import config_exists

try:
    from .config import secret_key, database_uri, debug_setting, remember_cookie_duration, sqlalchemy_track_modifications, image_extensions, document_extensions, imagekit_private_key, imagekit_public_key, imagekit_url_endpoint, max_content_length # allowed_extensions, upload_folder
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = database_uri
    DEBUG = debug_setting
    REMEMBER_COOKIE_DURATION = remember_cookie_duration
    SQLALCHEMY_TRACK_MODIFICATIONS = sqlalchemy_track_modifications
    # UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), upload_folder)
    IMAGE_EXTENSIONS = image_extensions
    DOCUMENT_EXTENSIONS = document_extensions
    # ALLOWED_EXTENSIONS = allowed_extensions
    MAX_CONTENT_LENGTH = max_content_length # reference: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

    # image kit
    IMAGEKIT_PRIVATE_KEY = imagekit_private_key
    IMAGEKIT_PUBLIC_KEY = imagekit_public_key
    IMAGEKIT_URL_ENDPOINT = imagekit_url_endpoint

except ImportError:
    pass


if os.environ.get("RDS_USERNAME"):
    # reference to variables: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/rds-external-defaultvpc.html [accessed: 16 April, 2023]
    SQLALCHEMY_DATABASE_URI= f'mysql+pymysql://{os.environ.get("RDS_USERNAME")}:{os.environ.get("RDS_PASSWORD")}@{os.environ.get("RDS_HOSTNAME")}:{os.environ.get("RDS_PORT")}/{os.environ.get("RDS_DB_NAME")}'

DEBUG = os.environ.get("DEBUG") if os.environ.get("DEBUG") else DEBUG
REMEMBER_COOKIE_DURATION = timedelta(days = int(os.environ.get("REMEMBER_COOKIE_DURATION"))) if os.environ.get("REMEMBER_COOKIE_DURATION") else REMEMBER_COOKIE_DURATION
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") if os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") else SQLALCHEMY_TRACK_MODIFICATIONS
# UPLOAD_FOLDER = 
# ALLOWED_EXTENSIONS = '' #{'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
IMAGE_EXTENSIONS = os.environ.get("IMAGE_EXTENSIONS") if os.environ.get("IMAGE_EXTENSIONS") else IMAGE_EXTENSIONS
DOCUMENT_EXTENSIONS = os.environ.get("DOCUMENT_EXTENSIONS") if os.environ.get("DOCUMENT_EXTENSIONS") else DOCUMENT_EXTENSIONS
MAX_CONTENT_LENGTH = os.environ.get("MAX_CONTENT_LENGTH") if os.environ.get("MAX_CONTENT_LENGTH") else MAX_CONTENT_LENGTH

# image kit
IMAGEKIT_PRIVATE_KEY = os.environ.get("IMAGEKIT_PRIVATE_KEY") if os.environ.get("IMAGEKIT_PRIVATE_KEY") else IMAGEKIT_PRIVATE_KEY
IMAGEKIT_PUBLIC_KEY = os.environ.get("IMAGEKIT_PUBLIC_KEY") if os.environ.get("IMAGEKIT_PUBLIC_KEY") else IMAGEKIT_PUBLIC_KEY
IMAGEKIT_URL_ENDPOINT = os.environ.get("IMAGEKIT_URL_ENDPOINT") if os.environ.get("IMAGEKIT_URL_ENDPOINT") else IMAGEKIT_URL_ENDPOINT


app = Flask(__name__)

# Note: Environment variables override the config.py file

# secret_key_setting
app.config['SECRET_KEY'] = SECRET_KEY

# database_setting
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# debug_setting
app.config['DEBUG'] = DEBUG

# remember_me_cookie_setting
app.config['REMEMBER_COOKIE_DURATION'] = REMEMBER_COOKIE_DURATION

# sqlalchemy_modifications_setting
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# sqlalchemy_modifications_setting
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# upload_folder_setting
# app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER") if os.environ.get("UPLOAD_FOLDER") else UPLOAD_FOLDER

# 
app.config['IMAGEKIT_PRIVATE_KEY'] = IMAGEKIT_PRIVATE_KEY

# 
app.config['IMAGEKIT_PUBLIC_KEY'] = IMAGEKIT_PUBLIC_KEY

# 
app.config['IMAGEKIT_URL_ENDPOINT'] = IMAGEKIT_URL_ENDPOINT

# 
app.config['IMAGE_EXTENSIONS'] = IMAGE_EXTENSIONS

# 
app.config['DOCUMENT_EXTENSIONS'] = DOCUMENT_EXTENSIONS

# 
app.config['ALLOWED_EXTENSIONS'] = IMAGE_EXTENSIONS + DOCUMENT_EXTENSIONS

# print(app.config['ALLOWED_EXTENSIONS'])



# Database setup with login featues 
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

# Image Kit SDK initialization
from imagekitio import ImageKit

imagekit = ImageKit(
    private_key = IMAGEKIT_PRIVATE_KEY,
    public_key = IMAGEKIT_PUBLIC_KEY,
    url_endpoint = IMAGEKIT_URL_ENDPOINT
)

# socketio setup
socketio = SocketIO(app)

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