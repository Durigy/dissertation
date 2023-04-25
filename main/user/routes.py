# from flask import Blueprint, render_template, abort
# from jinja2 import TemplateNotFound

from datetime import datetime
from .. import db, bcrypt, app
# import secrets
from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm, UpdateAccountForm, AddUniSchoolForm, AddUniYearForm, AddUniversityForm
from ..models import User, PublicProfile, University, UniversitySchool, UniversityYear, Module, MessageThread
from ..main_utils import generate_id, aside_dict


users = Blueprint('users', __name__, template_folder='templates')

#################################
#                               #
#           User Stuff          #
#                               #
#################################

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('index'))
    
    cardiff_uni_university = University.query.filter_by(name = 'Cardiff University').first()
    university_years = UniversityYear.query.order_by(UniversityYear.name).all()
    university_schools = UniversitySchool.query.order_by(UniversitySchool.name).all()

    form = RegistrationForm()
    if form.validate_on_submit() and request.method == "POST":
        user_id = generate_id(User) # pass the table name as a varible
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        profile_id = generate_id(PublicProfile)

        profile = PublicProfile(
            id = profile_id
        )

        user = User(
            id = user_id,
            username = form.username.data,
            firstname = form.firstname.data,
            lastname = form.lastname.data,
            email = form.email.data.lower() + '@cardiff.ac.uk',
            password = hashed_password,
            public_profile_id = profile_id,
            university_id = cardiff_uni_university.id,
            university_school_id = form.university_school.data,
            university_year_id = form.university_year.data,
        )

        db.session.add(user)
        db.session.add(profile)
        db.session.commit()
        flash('Account Created - You can now Login in')
        return redirect(url_for('users.login'))
    return render_template(
        'user/register.html',
        title='Register',
        form=form,
        university_schools = university_schools, 
        university_years = university_years
    )


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit() and request.method == "POST":
        user = ''
        if User.query.filter_by(username = form.username_email.data).first():
            user = User.query.filter_by(username = form.username_email.data).first()
        elif User.query.filter_by(email = form.username_email.data).first():
            user = User.query.filter_by(email = form.username_email.data).first()

        # user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("index"))
        else:
            flash('Login Unsuccessful. Check username/email and Password')

    return render_template(
        'user/login.html',
        title = 'Login',
        form = form
    )

@users.route("/logout")
def logout():
    logout_user()
    return redirect(request.referrer)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    
    if form.validate_on_submit() and request.method == "POST":

        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.username.data
        # current_user.email = form.email.data
        
        user_bio = form.bio.data
        
        if user_bio:
            if not current_user.public_profile_id:
                profile_id = generate_id(PublicProfile)

                profile = PublicProfile(
                    id = profile_id,
                    bio = user_bio
                )

                db.session.add(profile)
                current_user.profile = profile
            
            else:
                current_user.profile.bio = user_bio
                current_user.profile.date_edited = datetime.utcnow()

        db.session.commit()
        flash('Your account was updated')

        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username

        if current_user.profile:
            form.bio.data = current_user.profile.bio
        # form.email.data = current_user.email

    return render_template(
        'user/account.html',
        title='Account',
        form=form,
        my_aside_dict = aside_dict(current_user)
    )




# admin stuff thrown here #

# depricated route due to flask-admin, can be added back if needed
# @users.route(f"/{app.config['USER_CODE']}")
# @login_required
# def get_user_id():
#     if not current_user.is_admin:
#         flash('You don\'t have access to that')
#         return redirect(url_for('index'))
    
#     flash(f"You\'re user_id is: {current_user.id}")
#     return redirect(url_for('index'))

# depricated route due to flask-admin, can be added back if needed
# @users.route(f"/{app.config['ADMIN_CODE']}/<user_id>")
# @login_required
# def add_admin(user_id):
#     if not current_user.is_admin:
#         flash('You don\'t have access to that')
#         return redirect(url_for('index'))
    
#     user = User.query.get_or_404(user_id)

#     user.is_admin = True

#     db.session.commit()

#     flash("You are now an admin")
#     return redirect(url_for('modules.module_add'))


@users.route(f"/add-uni", methods=['GET', 'POST'])
@login_required
def admin_add_uni():
    """
    Route for an admin to add new Universities to the application
    """
    if not current_user.is_admin:
        flash('You don\'t have access to that')
        return redirect(url_for('index'))
    
    form = AddUniversityForm()

    if form.validate_on_submit() and request.method == "POST":
        university = University(
            id = generate_id(University),
            name = form.name.data
        )

        db.session.add(university)
        db.session.commit()

        flash('University added')
        return redirect(url_for('users.admin_add_uni'))
    
    return render_template(
        'user/add_uni_x.html',
        title='Add University',
        form=form,
        my_aside_dict = aside_dict(current_user)
    )

@users.route(f"/add-uni-year", methods=['GET', 'POST'])
@login_required
def admin_add_uni_year():
    """
    Route for an admin to add new University Years to the application
    """
    if not current_user.is_admin:
        flash('You don\'t have access to that')
        return redirect(url_for('index'))
    
    form = AddUniYearForm()

    if form.validate_on_submit() and request.method == "POST":
        university_year = UniversityYear(
            id = generate_id(UniversityYear),
            name = form.name.data
        )

        db.session.add(university_year)
        db.session.commit()

        flash('Year added')
        return redirect(url_for('users.admin_add_uni_year'))
    
    return render_template(
        'user/add_uni_x.html',
        title='Add Uni Year',
        form=form,
        my_aside_dict = aside_dict(current_user)
    )

@users.route(f"/add-uni-school", methods=['GET', 'POST'])
@login_required
def admin_add_uni_school():
    """
    Route for an admin to add new University Schools to the application
    """
    if not current_user.is_admin:
        flash('You don\'t have access to that')
        return redirect(url_for('index'))
    
    form = AddUniSchoolForm()

    if form.validate_on_submit() and request.method == "POST":
        university_school = UniversitySchool(
            id = generate_id(UniversitySchool),
            name = form.name.data            
        )

        db.session.add(university_school)
        db.session.commit()

        flash('School added')
        return redirect(url_for('users.admin_add_uni_school'))
    
    return render_template(
        'user/add_uni_x.html',
        title='Add Uni School',
        form=form,
        my_aside_dict = aside_dict(current_user)
    )

from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from .. import admin

class GoHomeLink(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('index'))
    
class UserView(ModelView):
    form_columns = ['id', 'username', 'firstname', 'lastname', 'email', 'is_admin', 'university_id', 'university_year_id', 'university_school_id', 'public_profile_id']
    can_view_details = True
    can_create = False
    column_editable_list = ['firstname', 'lastname', 'is_admin']

class UniversityView(ModelView):
    form_columns = ['id', 'name','url', 'date_established','first_line', 'second_line', 'city', 'country', 'postcode']
    can_view_details = True
    # can_edit = False
    can_create = False
    column_editable_list = ['name','url', 'first_line', 'second_line', 'city', 'country', 'postcode']

class ModuleView(ModelView):
    form_columns = ['id', 'name', 'code', 'description', 'tutor', 'university_id', 'university_school_id', 'university_year_id', 'message_thread_id']
    can_view_details = True
    # can_edit = False
    can_create = False
    column_editable_list = ['name', 'code', 'description', 'tutor']

class NameIdView(ModelView):
    form_columns = ['id', 'name']
    can_view_details = True
    # can_edit = False
    can_create = False
    column_editable_list = ['name']
    
# flask admin routes for adding databse tables to the view/delete in the admin panel (editing/adding can't be done here due to the dates)
admin.add_view(UserView(User, db.session))
admin.add_view(UniversityView(University, db.session))
admin.add_view(NameIdView(UniversitySchool, db.session))
admin.add_view(NameIdView(UniversityYear, db.session))
admin.add_view(ModuleView(Module, db.session))
admin.add_view(NameIdView(MessageThread, db.session))
admin.add_view(GoHomeLink(name='<- Back to site'))