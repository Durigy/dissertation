import secrets
from .models import Message, MessageThread, Module, ModuleQuestion, ModuleSubscription
from . import ALLOWED_EXTENSIONS

# reference to using addict: https://youtu.be/y7fZJDIU8V8?t=347 [accessed: 3 Apr 2023]
from addict import Dict

# this can be used for generating ids of string lenght 20 default
# or the default in modules can be used for small projects if preferred
def generate_id(query_table, id_length = 20):
    id = secrets.token_hex(round(abs(id_length/2)))

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


def defaults(current_user):
    module_list = Module.query.order_by(Module.code).all()

    subscribed_modules = ModuleSubscription.query.filter_by(user_id = current_user.id).join(Module).order_by(Module.name).all()

    taken_modules = ModuleSubscription.query.filter(ModuleSubscription.user_id == current_user.id).join(Module).order_by(Module.name).all()

    temp_list = []
    non_taking_modules = []

    for i in subscribed_modules:
        temp_list.append(i.module.id)

    for i in module_list:
        if i.id not in temp_list:
            non_taking_modules.append(i)

    return (
        module_list,
        subscribed_modules,
        non_taking_modules,
    )

def aside_dict(current_user):
    subscribed_modules = ModuleSubscription.query.filter_by(user_id = current_user.id).join(Module).order_by(Module.code).limit(10).all()
   
    questions = ModuleQuestion.query.filter(ModuleSubscription.user_id == current_user.id) \
            .filter_by(module_id = ModuleSubscription.module_id).filter_by(solved = False) \
            .filter(ModuleQuestion.user != current_user).filter_by(solved = False) \
            .order_by(ModuleQuestion.date.desc()).limit(10).all()
    
    message_threads = MessageThread.query.filter(MessageThread.following_user.contains(current_user)).order_by(MessageThread.date_last_message.desc()).all()
    
    # print(message_threads)
    return Dict({
        'subscribed_modules': subscribed_modules,
        'questions': questions,
        'message_threads': message_threads
    })

# taken from: https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/#a-gentle-introduction
def allowed_file(filename):
    """
    filename: incoming file name
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS