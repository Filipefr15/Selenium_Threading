lista = []

def list_receiver(list_from_function):
    global lista
    lista = list_from_function

def list_pop():
    global lista
    try:
        return int(lista.pop(0))
    except IndexError:
        raise
    
def list_is_none():
    global lista
    if lista is None:
        return True
    else:
        return False
    
def full_list():
    global lista
    return lista