from .. import db, bcrypt
from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user
from ..models import User

system = Blueprint('system', __name__, template_folder='templates')

#################################
#                               #
#          System Stuff         #
#                               #
#################################

# # this is only to be used on the production server for forcing the site to use https over http
# # reference: https://stackoverflow.com/questions/32237379/python-flask-redirect-to-https-from-http
# @system.before_request
# def before_request():
#     if not request.is_secure:
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)

@system.errorhandler(404)
def page_not_found(e):
    return render_template(
        'errors/404.html',
        title='404 error'
    )

@system.errorhandler(500)
def page_not_found(e):
    return render_template(
        'errors/500.html',
        title='500 error'
    )

@system.route('/')
def index():
    return render_template(
        'system/index.html',
        title='Home'
    )

# when '/home' or '/index' are typed in the URL or redirected, it will the redirect to the url without anything after the /
@system.route("/index")
@system.route("/home")
def home_redirect():
    return redirect(url_for('system.index'))


@system.route("/about")
@login_required
def about():
    return "hello from the about page"

@system.route("/contact", methods=['POST'])
@login_required
def contact():
    return "hello from the contact page"

