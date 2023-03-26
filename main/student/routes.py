from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
# from .forms import 
from ..models import User
from ..main_utils import generate_id

# referece: https://flask.palletsprojects.com/en/2.2.x/blueprints/#registering-blueprints
students = Blueprint('students', __name__, template_folder='templates',  url_prefix='/student') 

@students.route("")
@login_required
def student_home():
    return render_template(
        'student/student_home.html',
        title='Home'
    )

@students.route("/notes")
@login_required
def student_note():
    return render_template(
        'student/student_note.html',
        title='Notes'
    )

@students.route("/notes/<note_id>")
@login_required
def student_note_single(note_id):
    return render_template(
        'student/student_home.html',
        title='Single Note'
    )

@students.route("/my-modules")
@login_required
def student_modules():
    return render_template(
        'student/student_home.html',
        title='Modules'
    )

