from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from .forms import AddModuleForm
from ..models import User, Module, ModuleReview
from ..main_utils import generate_id
from .. import db

# referece: https://flask.palletsprojects.com/en/2.2.x/blueprints/#registering-blueprints
modules = Blueprint('modules', __name__, template_folder='templates',  url_prefix='/module') 

@modules.route("")
@login_required
def module_list():

    module_list = Module.query.order_by(Module.code).all()

    return render_template(
        'module/module_list.html',
        title='Home',
        modules = module_list
    )

@modules.route("/s/<module_id>")
@login_required
def module_single(module_id):
    module = Module.query.get_or_404(module_id)

    module_list = Module.query.order_by(Module.code).all()

    return render_template(
        'module/module_single.html',
        title = module.name,
        module = module
    )

@modules.route("/add", methods=['GET', 'POST'])
@login_required
def module_add():

    module_list = Module.query.order_by(Module.code).all()

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

        return redirect(url_for('modules.module_list'))

    return render_template(
        'module/module_add.html',
        title = "Add a new module",
        form = form,
        modules = module_list
    )

@modules.route("/s/<module_id>/reviews")
@login_required
def module_review_list(module_id):
    module = Module.query.get_or_404(module_id)

    module_list = Module.query.order_by(Module.code).all()

    module_reviews = ModuleReview.query.filter_by(module_id = module_id).order_by(ModuleReview.date_sent)

    return render_template(
        'module/module_reviews.html',
        title = f"{module.name} - Reviews",
        module = module,
        module_reviews = module_reviews,
        modules = module_list
    )

@modules.route("/questions")
@login_required
def module_question():
    module_list = Module.query.order_by(Module.code).all()

    return render_template(
        'module/module_question.html',
        title = "Questions",
        modules = module_list
    )
