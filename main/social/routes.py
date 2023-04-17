from flask import jsonify, render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user
from .forms import AddPostForm, AddPublicPostCommentForm
from ..models import Message, Module, User, PublicPost, PublicPostComment, MessageThread
from ..main_utils import generate_id, defaults, aside_dict
from .. import db

# referece: https://flask.palletsprojects.com/en/2.2.x/blueprints/#registering-blueprints
socials = Blueprint('socials', __name__, template_folder='templates',  url_prefix='/social') 

@socials.route("")
@login_required
def social_home():
    return render_template(
        'social/social_home.html',
        title='Socail Home',
        my_aside_dict = aside_dict(current_user)
    )

# @socials.route("posts")
# @login_required
# def social_post():
#     module_list, subscribed_modules, non_taking_modules = defaults(current_user)

#     return render_template(
#         'social/social_post.html',
#         title='Socail Posts',
#         module_list = module_list,
#         subscribed_modules = subscribed_modules,
#         non_taking_modules = non_taking_modules
#     )

# @socials.route("posts/add")
# @login_required
# def social_post_add():

#     # add post stuff here

#     return redirect(url_for(social_post))

############################
#                          #
#  Module Question Stuff   #
#                          #
############################

@socials.route("/posts")
@login_required
def social_post():
    # reference to my past code: https://github.com/Durigy/neighbourfy-v2/blob/main/main/routes.py [accessed: 1 April 2023]
    post_page = request.args.get('post_page', 1, type = int)
    posts = PublicPost.query \
        .order_by(PublicPost.date.desc()) \
        .paginate(page = post_page, per_page = 10)

    return render_template(
        'social/post/social_post_list.html',
        title = "Posts",
        my_aside_dict = aside_dict(current_user),
        posts = posts
    )

@socials.route("/posts/<post_id>", methods=['GET', 'POST'])
@login_required
def social_post_single(post_id):
    post = PublicPost.query.get_or_404(post_id)

    form = AddPublicPostCommentForm()

    comment_page = request.args.get('comment_page', 1, type = int)

    items_per_page = 10

    comments = PublicPostComment.query \
        .filter_by(public_post_id = PublicPost.id) \
        .order_by(PublicPostComment.date) \
        .paginate(page = comment_page, per_page = items_per_page)

    if form.validate_on_submit() and request.method == "POST":
        comment = PublicPostComment(
            id = generate_id(PublicPostComment),
            message = form.message.data,
            user_id = current_user.id,
            public_post_id = post_id
        )

        db.session.add(comment)

        comment_count = post.comment_count

        post.comment_count += 1

        db.session.commit()

        flash('Your Comment has been posted')

        # this checks how may items are on the last page. 
        # comments_2 = PublicPostComment.query \
        #     .filter_by(public_post_id = PublicPost.id) \
        #     .order_by(PublicPostComment.date) \
        #     .paginate(page = comments.pages, per_page = items_per_page)
        
        my_page = comments.pages if comment_count > 0 else 1
        
        # if there are 'items_per_page' number of items, then a new page will be created, so go to the new last page
        if len(comments.items) == items_per_page:
            my_page += 1
        
        return redirect(url_for('socials.social_post_single', post_id = post_id, comment_page = my_page))

    return render_template(
        'social/post/social_post_single.html',
        title = "Post",
        my_aside_dict = aside_dict(current_user),
        post = post,
        comments = comments,
        post_id = post_id,
        form = form
    )

@socials.route("/posts/add", methods = ["GET", "POST"])
@login_required
def social_post_add():
    form = AddPostForm()

    if form.validate_on_submit() and request.method == "POST":
        post_id = generate_id(PublicPost)

        post = PublicPost(
            id = post_id,
            title = form.title.data,
            description = form.description.data if len(form.description.data) > 0 else None,
            user_id = current_user.id
        )

        db.session.add(post)
        db.session.commit()

        flash('Your Post has been posted')
    
        return redirect(url_for('socials.social_post_single', post_id = post_id))

    return render_template(
        'social/post/social_post_add.html',
        title = "Add Post",
        my_aside_dict = aside_dict(current_user),
        form = form
    )

# @socials.route("/posts/<question_id>/remove")
# @login_required
# def social_question_remove(question_id):

#     return redirect(url_for)


############################
#                          #
#     Message Stuff        #
#                          #
############################

from sqlalchemy import func
@socials.route("messages")
@login_required
def social_message():
    count_by_thread_id = db.session.query(Message, func.count(Message.message_thread_id)) \
                       .group_by(Message.message_thread_id) \
                       .all()
    
    count_by_thread_id_dict = {message_thread_id.message_thread_id: count for message_thread_id, count in count_by_thread_id}
    # print(count_by_thread_id_dict)
    
    return render_template(
        'social/social_message_list.html',
        title='Socail Messages',
        my_aside_dict = aside_dict(current_user)
    )

@socials.route("/messages/<message_thread_id>")
@login_required
def social_message_single(message_thread_id):
    other_user_id = request.args.get('user_id')

    if other_user_id:
        thread = MessageThread.query.filter_by(id = message_thread_id).scalar()
    else:
        thread = MessageThread.query.get_or_404(message_thread_id)

    return render_template(
        'social/social_message_thread.html',
        title='Socail Messages',
        my_aside_dict = aside_dict(current_user),
        use_web_socket = True,
        socket_room = message_thread_id ,
        message_thread_id = message_thread_id,
        thread = thread,
        other_user_id = other_user_id
    )

@socials.route("/messages/new-thread/<user_id>")
@login_required
def social_message_thread_new(user_id):
    user = User.query.get_or_404(user_id)
    
    thread_id = generate_id(MessageThread)

    return redirect(url_for('socials.social_message_single', message_thread_id = thread_id, user_id = user_id))



@socials.route("/user-list")
@login_required
def social_user_list():
    users = User.query.filter(User.id != current_user.id).all()

    return render_template(
        'social/social_user_list.html',
        title='Socail Messages',
        my_aside_dict = aside_dict(current_user),
        users = users
    )

@socials.route("/messages/remove-thread/<thread_id>")
@login_required
def social_message_thread_remove(thread_id):
    # user = User.query.get_or_404(user_id)
    thread = MessageThread.query.filter_by(id = thread_id).first()

    for user in thread.following_user:
        user.in_thread.remove(thread)


    # current_user.in_thread.remove(thread)
    # user.in_thread.remove(thread)

    # print(thread)

    
    db.session.delete(thread)

    db.session.commit()

    return redirect(url_for('socials.social_user_list'))



############################
#                          #
#        Ajax Stuff        #
#                          #
############################

@socials.route("/get-messages/<message_thread_id>", methods=['GET'])
def social_get_messages(message_thread_id):

    message_thread = MessageThread.query.get_or_404(message_thread_id)

    message_page = request.args.get('message_page', 1, type = int)

    # print(message_page)

    messages = Message.query \
        .filter_by(message_thread_id = message_thread_id) \
        .order_by(Message.date_sent.desc()) \
        .paginate(page = message_page, per_page = 40)

    # if len(messages) > 0:
    response_messages = [{
        'next_page': message_page + 1 if message_page < messages.pages else messages.pages + 1,
        'total_pages': messages.pages
        }] +[{
            'user': message.user.username,
            'message': message.body,
            'datetime': str(message.date_sent.strftime('%I:%M, %d %b %Y')),
            'message_id': message.id
        } for message in messages.items
    ]

    return jsonify(
        response_messages
    )