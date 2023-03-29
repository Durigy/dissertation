from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
# from .forms import 
from ..models import User, Module, ModuleReview
from ..main_utils import generate_id, defaults
from .. import db

# referece: https://flask.palletsprojects.com/en/2.2.x/blueprints/#registering-blueprints
socials = Blueprint('socials', __name__, template_folder='templates',  url_prefix='/social') 

@socials.route("")
@login_required
def social_home():
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    return render_template(
        'social/social_home.html',
        title='Socail Home',
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )

@socials.route("posts")
@login_required
def social_post():
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    return render_template(
        'social/social_post.html',
        title='Socail Posts',
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )

@socials.route("posts/add")
@login_required
def social_post_add():

    # add post stuff here

    return redirect(url_for(social_post))

@socials.route("messages")
@login_required
def social_message():
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    return render_template(
        'social/social_message.html',
        title='Socail Messages',
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )

@socials.route("/messages/<thread_id>")
@login_required
def social_message_single(thread_id):
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    return render_template(
        'social/social_message_thread.html',
        title='Socail Messages',
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )