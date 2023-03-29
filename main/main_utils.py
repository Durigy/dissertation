import secrets
from .models import Module, ModuleSubscription

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