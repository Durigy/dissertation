from . import app, db, bcrypt
import secrets
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm, UpdateAccountForm
from .models import User


#################################
#                               #
#           Site Stuff          #
#                               #
#################################

# # this is only to be used on the production server for forcing the site to use https over http
# # reference: https://stackoverflow.com/questions/32237379/python-flask-redirect-to-https-from-http
# @app.before_request
# def before_request():
#     if not request.is_secure:
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)

@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'errors/404.html',
        title='404 error'
    )

@app.errorhandler(500)
def page_not_found(e):
    return render_template(
        'errors/500.html',
        title='500 error'
    )

@app.route('/')
def index():
    return render_template(
        'index.html',
        title='Home'
    )

# when '/home' or '/index' are typed in the URL or redirected, it will the redirect to the url without anything after the /
@app.route("/index")
@app.route("/home")
def home_redirect():
    return redirect(url_for('index'))

# this can be used for generating ids of string lenght 20 default
# or the default in modules can be used for small projects if preferred
def generate_id(query_table, id_length = 20):
    id = ''

    while True:
        if not check_id(query_table, id): 
            break
        id = secrets.token_hex(round(abs(id_length/2)))
    id = id[:id_length]
    
    return id

# returns true if no an id is found in the database
def check_id(query_table, query_id):
    ans = query_table.query.filter(query_table.id == query_id).first()
    return True if ans else False


#################################
#                               #
#           User Stuff          #
#                               #
#################################

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit() and request.method == "POST":
        # user_id = generate_id(User) # pass the table name as a varible
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(
            # id = user_id,
            username = form.username.data,
            firstname = form.firstname.data,
            lastname = form.lastname.data,
            email = form.email.data,
            password = hashed_password
        )

        db.session.add(user)
        db.session.commit()
        flash('Account Created - You can now Login in')
        return redirect(url_for('login'))
    return render_template(
        'user/register.html',
        title='Register',
        form=form
    )


@app.route("/login", methods=['GET', 'POST'])
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

@app.route("/logout")
def logout():
    logout_user()
    return redirect(request.referrer)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit() and request.method == "POST":

        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account was updated')

        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template(
        'user/account.html',
        title='Account',
        form=form
    )
