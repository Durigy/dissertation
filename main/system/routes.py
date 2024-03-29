from .. import db, bcrypt, app
from flask import render_template, url_for, request, redirect, flash, Blueprint, session
from flask_login import login_required, current_user
from ..models import User, Message, MessageThread
from ..main_utils import defaults, aside_dict, generate_id
from .. import socketio
from flask_socketio import emit, join_room, leave_room, send
from datetime import datetime
from time import sleep
import html

# system = Blueprint('system', __name__, template_folder='templates')

#################################
#                               #
#          System Stuff         #
#                               #
#################################

# # this is only to be used on the production server for forcing the site to use https over http
# # reference: https://stackoverflow.com/questions/32237379/python-flask-redirect-to-https-from-http
if app.config['DEBUG'] == False:
    @app.before_request
    def before_request():
        if not request.is_secure:
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

@app.errorhandler(404)
def page_not_found(e):
    if current_user.is_authenticated:
        my_aside_dict = aside_dict(current_user)
    else:
        my_aside_dict = {}

    return render_template(
        'errors/404.html',
        title='404 error',
        my_aside_dict = my_aside_dict
    )

@app.errorhandler(500)
def page_not_found(e):

    return render_template(
        'errors/500.html',
        title='500 error'
    )

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("students.student_home"))

    return render_template(
        'system/index.html',
        title='Home'
    )

# when '/home' or '/index' are typed into the URL or redirected, it will then redirect to the url without anything after the /
@app.route("/index")
@app.route("/home")
def home_redirect():
    return redirect(url_for('index'))


# @app.route("/about")
# @login_required
# def about():
#     return "hello from the about page"

# @app.route("/contact", methods=['POST'])
# @login_required
# def contact():
#     return "hello from the contact page"


@app.route('/privacy')
def privacy():

    return render_template(
        'system/privacy.html',
        title='Privacy'
    )


############################
#                          #
#     Web Socket Stuff     #
#                          #
############################

# sockectio #
@socketio.on('connect')
def connect(auth):
    # print('conneted')

    emit('message', {'message': 'You\'re connected', 'datetime': str(datetime.utcnow().strftime('%H:%M, %d %b %Y')), 'user': 'Server'})

@socketio.on('wake_up')
def wake_up(auth):
    # print('wake_up')

    emit('message', {'message': '', 'datetime': str(datetime.utcnow().strftime('%H:%M, %d %b %Y')), 'user': 'Server'})
    sleep(0.2)
    emit('message', {'message': '', 'datetime': str(datetime.utcnow().strftime('%H:%M, %d %b %Y')), 'user': 'Server'})
    sleep(0.2)
    emit('message', {'message': '', 'datetime': str(datetime.utcnow().strftime('%H:%M, %d %b %Y')), 'user': 'Server'})

@socketio.on('disconnect')
def disconnect():
    # print('Client disconnected')

    emit('message', {'message': 'You\'ve been disconnected', 'datetime': str(datetime.utcnow().strftime('%H:%M, %d %b %Y')), 'user': 'Server'})

@socketio.on('room-connect')
def room_connect(data):
    # print(data)

    if not data.get('user') == current_user.id:
        emit('message', {'message': 'Invalid user', 'datetime': str(datetime.utcnow().strftime('%H:%M, %d %b %Y')), 'user': 'Server'})
    room = data.get('room')

    join_room(room)

    emit('message', {'message': '', 'datetime': str(datetime.utcnow().strftime('%H:%M, %d %b %Y')), 'user': 'Server'})
    sleep(0.1)
    emit('message', {'message': '', 'datetime': str(datetime.utcnow().strftime('%H:%M, %d %b %Y')), 'user': 'Server'})

    # send({"user": 'Server', "message":f"{current_user.username} is here", 'datetime': str(datetime.utcnow().strftime('%H:%M, %d %b %Y'))}, to = room)

@socketio.on('message')
def message(data):
    # print(data)
    
    room = data.get('room')
    new_message = html.escape(data.get('message'))
    user_id = data.get('user_id') if data.get('user_id') else ''
    other_user_id = data.get('other_user_id') if data.get('other_user_id') else ''
    
    # print(new_message)

    print(MessageThread.query.filter_by(id = room).scalar())

    if not MessageThread.query.filter_by(id = room).first(): # == None:
        user = User.query.filter_by(id = user_id).first()
        other_user = User.query.filter_by(id = other_user_id).first()

        message_thread = MessageThread(
            id = room,
            name = f'{other_user.username} & {user.username}',
            user_id = user_id,
            member_count = 2
        )

        db.session.add(message_thread)

        user.in_thread.append(message_thread)
        other_user.in_thread.append(message_thread)

        db.session.commit()


    message_datetime = datetime.utcnow()

    content = {
        'user': data.get('user'),
        'message': new_message,
        'datetime': str(message_datetime.strftime('%H:%M, %d %b %Y'))
    }

    send(content, to = room)

    message_id = generate_id(Message)

    message = Message(
        id = message_id,
        user_id = data.get('user_id'),
        body = new_message,
        message_thread_id = data.get('room'),
        date_sent = message_datetime
    )

    thread = MessageThread.query.filter(MessageThread.id == room).first()

    db.session.add(message)
    
    thread.date_last_message = message_datetime
    thread.message_count += 1

    db.session.commit()

# @socketio.on('disconnet')
# def disconnet():
#     leave_room()


