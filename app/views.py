from flask import render_template, redirect, session, url_for, request, jsonify
from app import app, db, models, search
import config

@app.route('/index')
@app.route('/')
def hello():
    return render_template("introducing.html",title=config.AppName)

@app.errorhandler(404)
def not_found(error):
    return "Error 404"

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

@app.route("/buscar")
def buscarIndex():
    return render_template("buscar.html",title=config.AppName)

@app.route("/buscar/<busqueda>")
def buscar(busqueda):
    return str(search.searchFor(busqueda))


@app.route("/busqueda", methods=['POST'])
def busqueda():
    b = request.form['busqueda']
    u = search.searchFor(b)
    return "<span>"+str(u.nombre) + " , "+ str(u.descripcion) + "</span>"
