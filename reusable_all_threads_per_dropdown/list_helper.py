lista = []

def list_receiver(list_from_function):
    global list
    list = list_from_function

def list_pop():
    global list
    try:
        return int(list.pop(0))
    except IndexError:
        return IndexError
    
def list_is_none():
    global list
    if list is None:
        return True
    else:
        return False
    
def full_list():
    global list
    return list