import random

from flask import Blueprint
from flask import render_template, redirect, session, url_for, request, json

from app import models

mod = Blueprint('index', __name__, url_prefix=None)

@mod.route('/')
def index():
    return render_template("index.html")

@mod.route("/contacto")
def contact():
    return render_template("contact.html")



@mod.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] == config.adminUser and request.form['password'] == config.adminPass:
            session["logged"] = True
            return redirect(url_for("index.admin_link"))
        else:
            return 'Invalid username/password'
    return render_template('login.html')


@mod.route('/logout', methods=['POST', 'GET'])
def logout():
    session["logged"] = False
    return redirect(url_for("hello"))


@mod.route("/admin")
def admin_link():
    if tools.check_log():
        return tools.check_log()
    else:
        return render_template("panel/base.html")

@mod.route("/universidades")
def universities():
    retvar = models.University.query.all()
    random.shuffle(retvar)
    return render_template("oldViews/universities.html", universities=retvar)


@mod.route("/carreras")
def careers():
    retvar = models.Career.query.all()
    random.shuffle(retvar)
    return render_template("oldViews/careers.html", careers=retvar)


@mod.route("/universidades/<university>")
def universities_page(university):
    if " " in university:
        university = university.replace("-", " ")
        return redirect(url_for("buscar", busqueda=university))
    university = university.replace("-", " ")
    #u = models.University.query.filter(models.University.name.contains(university)).all()
    u = models.University.query.filter_by(name=university).all()
    #return str(len(u))
    if len(u) <= 0:
        return redirect(url_for("buscar", busqueda=university))
    else:
        return render_template("oldViews/university.html", university=u[0])


@mod.route("/carreras/<career>")
def careers_page(career):
    if " " in career:
        career = career.replace("-", " ")
        return redirect(url_for("buscar", busqueda=career))
    career = career.replace("-", " ")
    c = models.Career.query.filter_by(name=career).all()
    if len(c) <= 0:
        return redirect(url_for("buscar", busqueda=career))
    else:
        return render_template("oldViews/career.html", career=c[0])


@mod.route("/universidades/<university>/carreras/<career>")
def career_at_university_page(university, career):
    r = []
    if " " in career or " " in university:
        university = university.replace("-", " ")
        return redirect(url_for("buscar", busqueda=university))
    university = university.replace("-", " ")
    career = career.replace("-", " ")
    c = models.Career.query.filter_by(name=career).first()
    if isinstance(c, type(None)):
        return redirect(url_for("buscar", busqueda=university))
    s = models.CareerAtUniversity.query.filter_by(career_id=c.id).all()
    for sede in s:
        if sede.place.university.name == university:
            r.append(sede)
    return render_template("oldViews/career_at_university.html", careers=r)


@mod.route("/universidades/<university>/sedes/<campus>")
def campus_page(university, campus):
    if " " in university or " " in campus:
        university = university.replace("-", " ")
        return redirect(url_for("buscar", busqueda=university))
    university = university.replace("-", " ")
    campus = campus.replace("-", " ")
    c = models.UniversityHeadquarter.query.filter_by(campus_name=campus).all()
    for campus in c:
        if campus.university.name == university:
            return render_template("oldViews/campus.html", campus=campus)
    return redirect(url_for("404"))