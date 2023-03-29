from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from .forms import AddModuleForm
from ..models import User, Module, ModuleReview, ModuleSubscription
from ..main_utils import generate_id, defaults
from .. import db

# referece: https://flask.palletsprojects.com/en/2.2.x/blueprints/#registering-blueprints
modules = Blueprint('modules', __name__, template_folder='templates',  url_prefix='/module') 

@modules.route("")
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

# admin test stuff
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

        return redirect(url_for('modules.module_user_list'))

    return render_template(
        'module/module_add.html',
        title = "Add a new module",
        form = form,
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )

@modules.route("/s/<module_id>/reviews")
@login_required
def module_review_list(module_id):
    module = Module.query.get_or_404(module_id)

    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    module_reviews = ModuleReview.query.filter_by(module_id = module_id).order_by(ModuleReview.date_sent)

    return render_template(
        'module/module_reviews.html',
        title = f"{module.name} - Reviews",
        module = module,
        module_reviews = module_reviews,
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )

@modules.route("/questions")
@login_required
def module_question():
    module_list, subscribed_modules, non_taking_modules = defaults(current_user)

    return render_template(
        'module/module_question.html',
        title = "Questions",
        module_list = module_list,
        subscribed_modules = subscribed_modules,
        non_taking_modules = non_taking_modules
    )

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
