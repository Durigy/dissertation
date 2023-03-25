import secrets

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