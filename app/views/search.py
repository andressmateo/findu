from flask import Blueprint, request, redirect, render_template
from app import config
mod = Blueprint('search', __name__, url_prefix='/buscar')
@mod.route("/", methods=['POST', 'GET'])
def buscar_index():
    if request.method == 'POST':
        url = "/buscar/"+request.form['search']
        return redirect(url)
    return render_template("search.html", title=config.name)

@mod.route("/<busqueda>")
def buscar(busqueda):
    return render_template("search_list.html")
