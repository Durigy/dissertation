from flask import render_template, session, url_for, request, redirect, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from .. import IMAGEKIT_URL_ENDPOINT
# from .forms import 
from ..models import ModuleQuestion, ModuleResource, ModuleSubscription, PublicPost, User
from ..main_utils import generate_id, defaults, aside_dict

# referece: https://flask.palletsprojects.com/en/2.2.x/blueprints/#registering-blueprints
students = Blueprint('students', __name__, template_folder='templates',  url_prefix='/student') 

@students.route("")
@login_required
def student_home():
    # module resources
    resource_page = request.args.get('resource_page', 1, type = int)
    
    resources = ModuleResource.query \
        .filter(ModuleSubscription.user_id == current_user.id) \
        .filter_by(module_id = ModuleSubscription.module_id) \
        .order_by(ModuleResource.date.desc()) \
        .paginate(page = resource_page, per_page = 4)    

    user_question_page = request.args.get('user_question_page', 1, type = int)

    user_questions = ModuleQuestion.query \
        .filter_by(user_id = current_user.id) \
        .order_by(ModuleQuestion.date.desc()) \
        .paginate(page = user_question_page, per_page = 3)
    

    latest_question = ModuleQuestion.query.join(ModuleSubscription) \
        .filter(ModuleSubscription.user_id == current_user.id) \
        .filter(ModuleQuestion.user_id != current_user.id) \
        .filter_by(solved = False) \
        .order_by(ModuleQuestion.date.desc()) \
        .first()
    
    latest_post = PublicPost.query \
        .filter(PublicPost.user_id != current_user.id) \
        .order_by(PublicPost.date.desc()) \
        .first()
    
    return render_template(
        'student/student_home.html',
        title='Home',
        my_aside_dict = aside_dict(current_user),
        user_questions = user_questions,
        resources = resources,
        latest_question = latest_question,
        latest_post = latest_post,
        img_url = IMAGEKIT_URL_ENDPOINT + '/module-resource-image/',
        doc_url = IMAGEKIT_URL_ENDPOINT + '/module-resource-document/'
    )

@students.route("/notes")
@login_required
def student_note():
    return render_template(
        'student/student_note_list.html',
        title='Notes',
        my_aside_dict = aside_dict(current_user)
    )

@students.route("/notes/<note_id>")
@login_required
def student_note_single(note_id):
    return render_template(
        'student/student_home.html',
        title='Single Note',
        my_aside_dict = aside_dict(current_user)
    )

@students.route("/my-modules")
@login_required
def student_modules():
    return render_template(
        'student/student_home.html',
        title='Modules',
        my_aside_dict = aside_dict(current_user)
    )

