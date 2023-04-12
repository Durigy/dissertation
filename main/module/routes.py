from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user
from .forms import AddModuleForm, AddModuleQuestionForm, AddModuleQuestionCommentForm, AddModuleResourceForm
from ..models import User, Module, ModuleReview, ModuleSubscription, ModuleQuestion, ModuleQuestionComment, Image, Document, ModuleResource
from ..main_utils import generate_id, defaults, aside_dict, allowed_file
from .. import db, app, IMAGE_EXTENSIONS, DOCUMENT_EXTENSIONS, imagekit, IMAGEKIT_URL_ENDPOINT
import os
import base64
from tempfile import TemporaryDirectory
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

# referece: https://flask.palletsprojects.com/en/2.2.x/blueprints/#registering-blueprints
modules = Blueprint('modules', __name__, template_folder='templates',  url_prefix='/modules') 

@modules.route("/all")
@login_required
def module_all():
    module_list = Module.query.order_by(Module.code).all()

    return render_template(
        'module/module_list.html',
        title='Home',
        my_aside_dict = aside_dict(current_user),
        module_list = module_list
    )

@modules.route("/<module_id>")
@login_required
def module_single(module_id):
    module = Module.query.get_or_404(module_id)

    # module questions
    question_page = request.args.get('question_page', 1, type = int)
    
    questions = ModuleQuestion.query \
        .filter_by(module_id = module_id) \
        .order_by(ModuleQuestion.date.desc()) \
        .paginate(page = question_page, per_page = 3)

    # module resources
    resource_page = request.args.get('resource_page', 1, type = int)
    
    resources = ModuleResource.query \
        .filter_by(module_id = module_id) \
        .order_by(ModuleResource.date.desc()) \
        .paginate(page = resource_page, per_page = 4)

    return render_template(
        'module/module_single.html',
        title = module.name,
        module = module,
        my_aside_dict = aside_dict(current_user),
        questions = questions,
        module_id = module_id,
        resources = resources,
        img_url = IMAGEKIT_URL_ENDPOINT + '/module-resource-image/',
        doc_url = IMAGEKIT_URL_ENDPOINT + '/module-resource-document/'
    )

@modules.route("/image/<module_resource_id>")
@login_required
def module_image_view(module_resource_id):
    module_resource = ModuleResource.query.get_or_404(module_resource_id)

    module_image = module_resource.image

    return render_template(
        'module/module_image_view.html',
        title = module_resource.module.name,
        module = module_resource.module,
        my_aside_dict = aside_dict(current_user),
        module_id = module_resource.module_id,
        module_resource = module_resource,
        module_image = module_image,
        img_url = IMAGEKIT_URL_ENDPOINT + '/module-resource-image/'
    )

@modules.route("/document/<module_resource_id>")
@login_required
def module_document_view(module_resource_id):
    module_resource = ModuleResource.query.get_or_404(module_resource_id)

    module_document = module_resource.document

    return render_template(
        'module/module_document_view.html',
        title = module_resource.module.name,
        module = module_resource.module,
        my_aside_dict = aside_dict(current_user),
        module_id = module_resource.module_id,
        module_resource = module_resource,
        module_document = module_document,
        doc_url = IMAGEKIT_URL_ENDPOINT + '/module-resource-document/'
    )

@modules.route("/<module_id>/reviews")
@login_required
def module_review_list(module_id):
    module = Module.query.get_or_404(module_id)

    module_reviews = ModuleReview.query.filter_by(module_id = module_id).order_by(ModuleReview.date_sent).all()

    return render_template(
        'module/module_reviews.html',
        title = f"{module.name} - Reviews",
        module = module,
        module_reviews = module_reviews,
        my_aside_dict = aside_dict(current_user)
    )


############################
#                          #
#  Module Question Stuff   #
#                          #
############################

@modules.route("/questions")
@login_required
def module_question():
    # # reference: https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending [accessed: 1 April 2023]
    # questions = ModuleQuestion.query.filter_by(module_id = ModuleSubscription.module_id).order_by(ModuleQuestion.date.desc()).all()

    # reference to my past code: https://github.com/Durigy/neighbourfy-v2/blob/main/main/routes.py [accessed: 1 April 2023]
    question_page = request.args.get('question_page', 1, type = int)

    questions = ModuleQuestion.query \
        .filter(ModuleSubscription.user_id == current_user.id) \
        .filter_by(module_id = ModuleSubscription.module_id) \
        .order_by(ModuleQuestion.date.desc()) \
        .paginate(page = question_page, per_page = 5)
    

    user_question_page = request.args.get('user_question_page', 1, type = int)

    user_questions = ModuleQuestion.query \
        .filter_by(user_id = current_user.id) \
        .order_by(ModuleQuestion.date.desc()) \
        .paginate(page = user_question_page, per_page = 3)
    
    return render_template(
        'module/module_question_list.html',
        title = "Questions",
        my_aside_dict = aside_dict(current_user),
        questions = questions,
        user_questions = user_questions
    )

@modules.route("/questions/<question_id>", methods=['GET', 'POST'])
@login_required
def module_question_single(question_id):
    question = ModuleQuestion.query.get_or_404(question_id)

    module = Module.query.filter_by(id = question.module_id).first()

    form = AddModuleQuestionCommentForm()

    comment_page = request.args.get('comment_page', 1, type = int)

    items_per_page = 10

    comments = ModuleQuestionComment.query \
        .filter_by(module_question_id = question_id) \
        .order_by(ModuleQuestionComment.date_sent) \
        .paginate(page = comment_page, per_page = items_per_page)

    if form.validate_on_submit() and request.method == "POST":
        message = ModuleQuestionComment(
            id = generate_id(ModuleQuestionComment),
            message = form.message.data,
            user_id = current_user.id,
            module_question_id = question_id
        )

        db.session.add(message)
        db.session.commit()

        flash('Your Comment has been posted')

        my_page = comments.pages
        
        # if there are 'items_per_page' number of items, then a new page will be created, so go to the new last page
        if len(comments.items) == items_per_page:
            my_page += 1
        
        return redirect(url_for('modules.module_question_single', question_id = question_id, comment_page = my_page))

    return render_template(
        'module/module_question_single.html',
        title = "Question",
        my_aside_dict = aside_dict(current_user),
        question = question,
        module = module,
        comments = comments,
        question_id = question_id,
        form = form
    )

@modules.route("/questions/<question_id>/solved", methods = ["GET", "POST"])
@login_required
def module_question_solved(question_id):
    question = ModuleQuestion.query.get_or_404(question_id)
    if question.user_id != current_user.id:
        flash('Sorry you don\'t have access to that!')
        return redirect(url_for('modules.module_question_single', question_id = question_id))

    question.solved = True
    db.session.commit()
    flash('The question have now been soved')
    return redirect(url_for('modules.module_question_single', question_id = question_id))



@modules.route("/questions/add", methods = ["GET", "POST"])
@login_required
def module_question_add():
    form = AddModuleQuestionForm()

    # reference: https://werkzeug.palletsprojects.com/en/0.14.x/datastructures/#werkzeug.datastructures.MultiDict.get [accessed: 1 April 2023]
    module_id = request.args.get('module_id', default = None, type = str)

    if form.validate_on_submit() and request.method == "POST":
        question_id = generate_id(ModuleQuestion)
        module_id = request.form.get('module')

        question = ModuleQuestion(
            id = question_id,
            title = form.title.data,
            description = form.description.data if len(form.description.data) > 0 else None,
            user_id = current_user.id,
            module_id = module_id 
        )

        db.session.add(question)
        db.session.commit()

        flash('Your Question has been posted')
    
        return redirect(url_for('modules.module_question_single', question_id = question_id))

    return render_template(
        'module/module_question_add.html',
        title = "Questions",
        my_aside_dict = aside_dict(current_user),
        form = form,
        module_id = module_id
    )

# @modules.route("/questions/<question_id>/remove")
# @login_required
# def module_question_remove(question_id):



#     return redirect(url_for)


############################
#                          #
#  Module selection stuff  #
#                          #
############################

@modules.route("/mine")
@login_required
def module_user_list():
    subscribed_modules = ModuleSubscription.query.filter_by(user_id = current_user.id).join(Module).order_by(Module.name).all()

    return render_template(
        'module/module_user_list.html',
        title = "My Modules",
        my_aside_dict = aside_dict(current_user),
        subscribed_modules = subscribed_modules
    )

@modules.route("/selection")
@login_required
def module_selection():
    module_list = Module.query.order_by(Module.code).all()

    subscribed_modules = ModuleSubscription.query.filter_by(user_id = current_user.id).join(Module).order_by(Module.name).all()

    # taken_modules = ModuleSubscription.query.filter(ModuleSubscription.user_id == current_user.id).join(Module).order_by(Module.name).all()

    temp_list = []
    non_taking_modules = []

    for i in subscribed_modules:
        temp_list.append(i.module.id)

    for i in module_list:
        if i.id not in temp_list:
            non_taking_modules.append(i)

    return render_template(
        'module/module_selection.html',
        title = "My Modules",
        my_aside_dict = aside_dict(current_user),
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )

@modules.route("/add-sub/<module_id>")
@login_required
def module_add_sub(module_id):
    module = Module.query.get_or_404(module_id)

    if bool(ModuleSubscription.query.filter_by(user_id = current_user.id, module_id = module_id).first()) == False:
        add_module = ModuleSubscription(
            id = generate_id(User),
            user_id = current_user.id,
            module_id = module_id
        )

        db.session.add(add_module)
        db.session.commit()

        flash('Now Subed to the Module')

        return redirect(url_for('modules.module_selection'))
    
    flash('Already Subed to the Module')

    return redirect(url_for('modules.module_selection'))

@modules.route("/remove-sub/<module_id>")
@login_required
def module_remove_sub(module_id):
    module = ModuleSubscription.query.filter_by(user_id=current_user.id, module_id=module_id).first()

    db.session.delete(module)
    db.session.commit()

    flash('Unsubed from Module')

    return redirect(url_for('modules.module_selection'))


############################
#                          #
#  Module Resource Stuff   #
#                          #
############################

@modules.route("/resource/add", methods = ["GET", "POST"])
@login_required
def module_resource_add():
    form = AddModuleResourceForm()

    # reference: https://werkzeug.palletsprojects.com/en/0.14.x/datastructures/#werkzeug.datastructures.MultiDict.get [accessed: 1 April 2023]
    module_id = request.args.get('module_id', default = None, type = str)

    if form.validate_on_submit() and request.method == "POST":
        module_id = request.form.get('module')

        file = form.file.data

        if file:
            if allowed_file(file.filename):
                module_file_id = generate_id(ModuleResource)
                
                file_type = file.filename.rsplit('.', 1)[1].lower()

                if file_type in IMAGE_EXTENSIONS:
                    image_id = generate_id(Image)
                    
                    filename = image_id +'.' + file_type
                
                    # references: 
                    # - https://youtu.be/-pmgCmWiOXo
                    # - https://docs.python.org/3/library/tempfile.html
                    with TemporaryDirectory() as temp_dir:
                        file.save(temp_dir + '/' + filename)

                        with open(temp_dir + '/' + filename, mode="rb") as temp:
                            filestr = base64.b64encode(temp.read())
                        print(temp_dir)
                        print(temp_dir + '/' + filename)

                    upload = imagekit.upload_file(
                        file = filestr,
                        file_name = filename,
                        options=UploadFileRequestOptions(
                            folder='/module-resource-image/',
                            is_private_file=False,
                        )
                    )

                    file_table = Image(
                        id = image_id,
                        title = form.title.data,
                        description = form.description.data if len(form.description.data) > 0 else None,
                        user_id = current_user.id,
                        imagekit_id = upload.name,
                        file_type = file_type
                    )

                    module_resource = ModuleResource(
                        id = module_file_id,
                        user_id = current_user.id,
                        module_id = module_id,
                        image_id = image_id
                    )

                else:
                    document_id = generate_id(Document)

                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'docs', filename))
                    
                    filename = document_id +'.' + file_type
                
                    # references: 
                    # - https://youtu.be/-pmgCmWiOXo
                    # - https://docs.python.org/3/library/tempfile.html
                    with TemporaryDirectory() as temp_dir:
                        file.save(temp_dir + '/' + filename)

                        with open(temp_dir + '/' + filename, mode="rb") as temp:
                            filestr = base64.b64encode(temp.read())

                    upload = imagekit.upload_file(
                        file = filestr,
                        file_name = filename,
                        options=UploadFileRequestOptions(
                            folder='/module-resource-document/',
                            is_private_file=False,
                        )
                    )

                    file_table = Document(
                        id = document_id,
                        title = form.title.data,
                        description = form.description.data if len(form.description.data) > 0 else None,
                        user_id = current_user.id,
                        imagekit_id = upload.name,
                        file_type = file_type
                    )

                    module_resource = ModuleResource(
                        id = module_file_id,
                        user_id = current_user.id,
                        module_id = module_id,
                        document_id = document_id
                    )


                db.session.add(file_table)
                db.session.add(module_resource)

                db.session.commit()

                if module_id:
                    return redirect(url_for('modules.module_single', module_id = module_id))

                return redirect(url_for('modules.module_resource_add'))
            else:
                flash('File type not allowed')


    return render_template(
        'module/module_resource_add.html',
        title = "Questions",
        my_aside_dict = aside_dict(current_user),
        form = form,
        module_id = module_id
    )


############################
#                          #
#     Admin Test Stuff     #
#                          #
############################

@modules.route("/add", methods=['GET', 'POST'])
@login_required
def module_add():
    form = AddModuleForm()

    if form.validate_on_submit() and request.method == "POST":
        module = Module(
            id = generate_id(Module),
            name = form.name.data,
            code = form.code.data,
            description = form.description.data if len(form.description.data) > 0 else None
        )

        db.session.add(module)
        db.session.commit()

        flash('The module was added')

        return redirect(url_for('modules.module_add'))

    return render_template(
        'module/module_add.html',
        title = "Add a new module",
        form = form,
        my_aside_dict = aside_dict(current_user)
    )
