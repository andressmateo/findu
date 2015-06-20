from flask import render_template
from app import app, models

@app.errorhandler(404)
def not_found(error=""):
    print error
    return render_template("oldViews/404.html")

@app.errorhandler(500)
def not_found(error):
    print error
    return render_template("oldViews/404.html")

@app.template_global()
def if_none(original, remplace):
    if isinstance(original, type(None)):
        return remplace
    elif (original == "" or original==-1):
        return remplace
    else:
        return original

@app.template_global()
def is_knowledge_area(question):
    if isinstance(question, models.KnowledgeArea):
        return True

@app.template_global()
def is_university(question):
    if isinstance(question, models.University):
        return True

@app.template_global()
def is_career(question):
    if isinstance(question, models.Career):
        return True

@app.template_global()
def join_campus(university):
    careers = []
    for u in university.places.all():
        for cu in u.careers.all():
            careers.append(cu.career)
    return list(set(careers))

@app.template_global()
def join_universities_from_campuses(campuses):
    return list(set([x.place.university for x in campuses]))

