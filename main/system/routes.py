from .. import db, bcrypt, app
from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user
from ..models import User
from ..main_utils import defaults, aside_dict

# system = Blueprint('system', __name__, template_folder='templates')

#################################
#                               #
#          System Stuff         #
#                               #
#################################

# # this is only to be used on the production server for forcing the site to use https over http
# # reference: https://stackoverflow.com/questions/32237379/python-flask-redirect-to-https-from-http
# @app.before_request
# def before_request():
#     if not request.is_secure:
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)

@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'errors/404.html',
        title='404 error',
        my_aside_dict = aside_dict(current_user)
    )

@app.errorhandler(500)
def page_not_found(e):

    return render_template(
        'errors/500.html',
        title='500 error'
    )

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("students.student_home"))

    return render_template(
        'system/index.html',
        title='Home'
    )

# when '/home' or '/index' are typed into the URL or redirected, it will then redirect to the url without anything after the /
@app.route("/index")
@app.route("/home")
def home_redirect():
    return redirect(url_for('index'))


@app.route("/about")
@login_required
def about():
    return "hello from the about page"

@app.route("/contact", methods=['POST'])
@login_required
def contact():
    return "hello from the contact page"

