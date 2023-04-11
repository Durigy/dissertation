from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, current_user
from .forms import AddPostForm, AddPublicPostCommentForm
from ..models import User, PublicPost, PublicPostComment
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
        message = PublicPostComment(
            id = generate_id(PublicPostComment),
            message = form.message.data,
            user_id = current_user.id,
            public_post_id = post_id
        )

        db.session.add(message)
        db.session.commit()

        flash('Your Comment has been posted')

        # this checks how may items are on the last page. 
        comments_2 = PublicPostComment.query \
            .filter_by(public_post_id = PublicPost.id) \
            .order_by(PublicPostComment.date) \
            .paginate(page = comments.pages, per_page = items_per_page)

        my_page = comments.pages
        
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

@socials.route("messages")
@login_required
def social_message():
    return render_template(
        'social/social_message_list.html',
        title='Socail Messages',
        my_aside_dict = aside_dict(current_user)
    )

@socials.route("/messages/<thread_id>")
@login_required
def social_message_single(thread_id):
    return render_template(
        'social/social_message_thread.html',
        title='Socail Messages',
        my_aside_dict = aside_dict(current_user)
    )
