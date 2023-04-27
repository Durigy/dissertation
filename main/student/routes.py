from datetime import datetime
from flask import render_template, session, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user

from .. import db
from .. import IMAGEKIT_URL_ENDPOINT
from .forms import CreateNoteForm
from ..models import ModuleQuestion, ModuleResource, ModuleSubscription, PublicPost, User, Note
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
    
    latest_question = ModuleQuestion.query \
        .filter(ModuleQuestion.user_id != current_user.id) \
        .filter_by(solved = False) \
        .join(ModuleSubscription, ModuleSubscription.module_id == ModuleQuestion.module_id) \
        .filter(ModuleSubscription.user_id == current_user.id) \
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

@students.route("/my-modules")
@login_required
def student_modules():
    return render_template(
        'student/student_home.html',
        title='Modules',
        my_aside_dict = aside_dict(current_user)
    )

@students.route("/notes")
@login_required
def student_note():
    notes = Note.query.filter_by(user_id = current_user.id).order_by(Note.date_edited.desc()).all()

    return render_template(
        'student/student_note_list.html',
        title='Notes',
        my_aside_dict = aside_dict(current_user),
        notes = notes
    )

@students.route("/notes/<note_id>", methods = ['GET', 'POST'])
@login_required
def student_note_single(note_id):

    form = CreateNoteForm()

    if request.method == "GET":
        if request.args.get('new'):
            note = ''
            module_select_id = request.args.get('module_id') if request.args.get('module_id') else ''

        else:
            note = Note.query.get_or_404(note_id)
            print(note.title)
            form.title.data = note.title
            form.text.data = note.text
            module_select_id = note.module_id

    elif form.validate_on_submit() and request.method == "POST":
        form_title = form.title.data
        form_text = form.text.data
        form_module_id = request.form.get('module_select')

        # print(form.title.data)


        # print(form_module_id)
        
        # if not (title or text):
        #     return redirect(url_for('students.student_note_single', note_id = 'new', new = 'true'))
        
        # note_id = ''
        
        if request.args.get('new'):
            note_id = generate_id(Note)

            note = Note(
                id = note_id,
                title = form.title.data,
                text = form_text,
                user_id = current_user.id,
                module_id = form_module_id if not form_module_id == '' else None
            )

            db.session.add(note)
        
        else:
            note = Note.query.filter_by(id = note_id).first()

            note.title = form_title
            note.text = form_text
            note.date_edited = datetime.utcnow()
            note.module_id = form_module_id if not form_module_id == '' else None
            note_id = note.id

        db.session.commit()
        
        # form_title = form.title.data
        # form_text = form.text.data
        # form_module_id = form_module_id

        flash('Your note was Saved')
        return redirect(url_for('students.student_note_single', note_id = note_id))
    


    # form.title.data = note.title
    # form.text.data = note.text
    # module_select_id = note.module_id

    return render_template(
        'student/student_note_single.html',
        title='Single Note',
        my_aside_dict = aside_dict(current_user),
        note = note,
        form = form,
        module_select_id = module_select_id,
        request = request
    )
