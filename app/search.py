
from app import Universidad

tags = ['Universidad Nacional', 'nacho', 'unal', 'Nacional']

u = Universidad.Universidad(1, "Universidad Nacional", "Es una buena universidad")
v = Universidad.Universidad(1, "Por favor ingresa un nombre correcto", "gracias")


def busqueda(b):
    r = v
    for t in tags:
        if b == t:
            r = u
    return r

