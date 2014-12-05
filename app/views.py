from flask import render_template, redirect, session, url_for, request, jsonify
from app import app, db
import config

@app.route('/index')
@app.route('/')
def hello():
    return 'Deployment...'

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def not_found(error):
    return render_template("404.html"), 500

#Ejemplo de Obtener datos de una Ruta
@app.route("/w/<name>")
def helname(name):
    return "Hello {}!".format(name)

@app.route("/id/<int:name>")
def idpage(name):
    return str(name)