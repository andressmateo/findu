# -*- coding: utf-8 -*-
from flask import render_template, redirect, session, url_for, request, jsonify
from app import app, db, models, search
import config


#OTHER ONES
def check_log():
    if not session["logged"]:
        return redirect(url_for("login"))
#VIEWS
@app.route('/index')
@app.route('/')
def hello():
    return render_template("introducing.html", config=config)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")

@app.errorhandler(500)
def not_found(error):
    return "Error 500"

#Ejemplo de Obtener datos de una Ruta
@app.route("/w/<name>")
def helname(name):
    return "Hello {}!".format(name)

@app.route("/id/<int:name>")
def idpage(name):
    return str(name)

##LLAMANDO la Base de Datos :D
@app.route("/Team")
def team():
    ret = ""
    for member in models.Team.query.all():
        ret += "<span>"+str(member.username)+"|"+str(member.age)+"</span><br/>"
    return ret

@app.route("/buscar", methods=['POST', 'GET'])
def buscarIndex():
    if request.method == 'POST':
        url = "/buscar/"+request.form['busqueda']
        return redirect(url)
        #return url
    return render_template("search.html",title=config.AppName)

@app.route("/buscar/<busqueda>")
def buscar(busqueda):
    result = search.searchFor(busqueda)
    if (isinstance(result,models.University)):
        return render_template("university.html",university = result)
    elif (isinstance(result,models.Career)):
        return str(result.name)
    else:
        return str(result)

@app.route("/contacto")
def contact():
    return "No hay"

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] == config.adminUser and request.form['password'] == config.adminPass:
            session["logged"] = True
            return redirect(url_for("admin_link"))
        else:
            return 'Invalid username/password'
    return render_template('login.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session["logged"] = False
    return  redirect(url_for("hello"))

@app.route("/admin")
def admin_link():
    if check_log():
        return check_log()
    else:
        return "Inside"

@app.route("/panel")
def panel():
    if check_log():
        return check_log()
    else:
        return "Making a Panel"

@app.route("/panel/add/")
def panel_add():
    if check_log():
        return check_log()
    else:
        return "What do you want to add?"

@app.route("/panel/add/university", methods=['POST', 'GET'])
def panel_add_university():
    if check_log():
        return check_log()
    else:
        if request.method == 'POST':
            if request.form["name"] and request.form["description"] and request.form["logo"]:
                try:
                    university = models.University(request.form["name"],
                                                   request.form["description"], request.form["logo"])
                    db.session.add(university)
                    db.session.commit()
                    return render_template("form_result.html", success=True)
                except:
                    return render_template("form_result.html", error=True)
            else:
                return render_template("form_result.html", error=True)
        else:
            return render_template("form_university.html")

@app.route("/list/university")
def list_university():
    all = models.University.query.all()
    #Temporaly I'm going to change this
    ret = ""
    for university in all:
        ret += "<p>"+str(university.id)+university.name+university.description+university.logo+"</p><br>"
    return ret
@app.route("/test")
def test():
        return render_template("form_result.html",success=True)