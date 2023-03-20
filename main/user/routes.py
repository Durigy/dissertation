# from flask import Blueprint, render_template, abort
# from jinja2 import TemplateNotFound

from .. import db, bcrypt
# import secrets
from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm, UpdateAccountForm
from ..models import User
from ..main_utils import generate_id


users = Blueprint('users', __name__, template_folder='templates')

#################################
#                               #
#           User Stuff          #
#                               #
#################################

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit() and request.method == "POST":
        user_id = generate_id(User) # pass the table name as a varible
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(
            id = user_id,
            username = form.username.data,
            firstname = form.firstname.data,
            lastname = form.lastname.data,
            email = form.email.data,
            password = hashed_password
        )

        db.session.add(user)
        db.session.commit()
        flash('Account Created - You can now Login in')
        return redirect(url_for('users.login'))
    return render_template(
        'user/register.html',
        title='Register',
        form=form
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
        db.session.commit()
        flash('Your account was updated')

        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        # form.email.data = current_user.email

    return render_template(
        'user/account.html',
        title='Account',
        form=form
    )