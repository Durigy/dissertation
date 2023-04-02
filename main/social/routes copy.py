from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user
from .forms import AddModuleForm, AddModuleQuestionForm, AddModuleQuestionCommentForm
from ..models import User, Module, ModuleReview, ModuleSubscription, ModuleQuestion, ModuleQuestionComment
from ..main_utils import generate_id, defaults
from .. import db

# referece: https://flask.palletsprojects.com/en/2.2.x/blueprints/#registering-blueprints
modules = Blueprint('modules', __name__, template_folder='templates',  url_prefix='/modules') 

@modules.route("/all")
@login_required
def module_all():
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    return render_template(
        'module/module_list.html',
        title='Home',
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )

@modules.route("/<module_id>")
@login_required
def module_single(module_id):
    module = Module.query.get_or_404(module_id)

    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    return render_template(
        'module/module_single.html',
        title = module.name,
        module = module,
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )

@modules.route("/<module_id>/reviews")
@login_required
def module_review_list(module_id):
    module = Module.query.get_or_404(module_id)

    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    module_reviews = ModuleReview.query.filter_by(module_id = module_id).order_by(ModuleReview.date_sent).all()

    return render_template(
        'module/module_reviews.html',
        title = f"{module.name} - Reviews",
        module = module,
        module_reviews = module_reviews,
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )


############################
#                          #
#  Module Question Stuff   #
#                          #
############################

@modules.route("/questions")
@login_required
def module_question():
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    # # reference: https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending [accessed: 1 April 2023]
    # questions = ModuleQuestion.query.filter_by(module_id = ModuleSubscription.module_id).order_by(ModuleQuestion.date.desc()).all()

    # reference to my past code: https://github.com/Durigy/neighbourfy-v2/blob/main/main/routes.py [accessed: 1 April 2023]
    module_page = request.args.get('module_page', 1, type = int)
    questions = ModuleQuestion.query \
        .filter_by(module_id = ModuleSubscription.module_id) \
        .order_by(ModuleQuestion.date.desc()) \
        .paginate(page = module_page, per_page = 10)

    return render_template(
        'module/module_question_list.html',
        title = "Questions",
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules,
        questions = questions
    )

@modules.route("/questions/<question_id>", methods=['GET', 'POST'])
@login_required
def module_question_single(question_id):
    question = ModuleQuestion.query.get_or_404(question_id)

    module = Module.query.filter_by(id = question.module_id).first()

    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    form = AddModuleQuestionCommentForm()

    comment_page = request.args.get('comment_page', 1, type = int)

    items_per_page = 10

    comments = ModuleQuestionComment.query \
        .filter_by(module_question_id = ModuleQuestion.id) \
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

        # this checks how may items are on the last page. 
        comments_2 = ModuleQuestionComment.query \
            .filter_by(module_question_id = ModuleQuestion.id) \
            .order_by(ModuleQuestionComment.date_sent) \
            .paginate(page = comments.pages, per_page = items_per_page)

        my_page = comments.pages
        
        # if there are 'items_per_page' number of items, then a new page will be created, so go to the new last page
        if len(comments_2.items) == items_per_page:
            my_page += 1
        
        return redirect(url_for('modules.module_question_single', question_id = question_id, comment_page = my_page))

    return render_template(
        'module/module_question_single.html',
        title = "Question",
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules,
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
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    form = AddModuleQuestionForm()

    # reference: https://werkzeug.palletsprojects.com/en/0.14.x/datastructures/#werkzeug.datastructures.MultiDict.get [accessed: 1 April 2023]
    selected_module_id = request.args.get('selected_module', default = None, type = str)

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
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules,
        form = form,
        selected_module_id = selected_module_id
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
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    return render_template(
        'module/module_user_list.html',
        title = "My Modules",
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )

@modules.route("/selection")
@login_required
def module_selection():
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    return render_template(
        'module/module_selection.html',
        title = "My Modules",
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
#     admin test stuff     #
#                          #
############################

@modules.route("/add", methods=['GET', 'POST'])
@login_required
def module_add():
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

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
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )
