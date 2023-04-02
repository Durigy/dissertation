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

@modules.route("/s/<module_id>")
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

@modules.route("/s/<module_id>/reviews")
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

    # reference: https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending [accessed: 1 April 2023]
    questions = ModuleQuestion.query.filter_by(module_id = ModuleSubscription.module_id).order_by(ModuleQuestion.date.desc()).all()

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

    # if form.validate_on_submit() and request.method == "POST":
    #     question = ModuleQuestionComment(
    #         id = generate_id(ModuleQuestionComment),
    #         title = form.title.data,
    #         description = form.description.data if len(form.description.data) > 0 else None
    #     )

    #     db.session.add(question)
    #     db.session.commit()

    #     flash('Your Question has been posted')
    
    #     return redirect(url_for('modules.module_question_single', question_id = question_id))

    return render_template(
        'module/module_question_single.html',
        title = "Question",
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules,
        question = question,
        module = module
    )

@modules.route("/questions/add", methods = ["GET", "POST"])
@login_required
def module_question_add():
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    form = AddModuleQuestionForm()

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
        form = form
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
