from app import models, app, db

def searchFor(b):
    ret ="Lo sentimos, no se encontraron resultados"
    for u in models.OtherName.query.filter_by(name = b):
            ret = "<span>"+str(u.name)+"-"+(u.university.name).encode('utf-8')+"</span><br/>"
    return ret