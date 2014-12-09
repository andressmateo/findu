
from app import Universidad

tags = ['Universidad Nacional','nacho','unal','Nacional']

u = Universidad.Universidad(1,"Universidad Nacional","Es una buena universidad")

def busqueda(b):
    r = False
    for t in tags:
        if b == t:
            r = u
    return r

