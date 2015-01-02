# -*- coding: utf-8 -*-
from flask import render_template, redirect, session, url_for, request, jsonify
from app import app, db, models, search
import config


#OTHER ONES
def check_log():
    if not session["logged"]:
        return redirect(url_for("login"))


def university_json():
    result = models.University.query.all()
    result_json = []
    for university in result:
        u = {
            "id": university.id,
            "name": university.name,
            "description": university.description,
            "logo": university.logo
        }
        result_json.append(u)
    return jsonify(university=result_json)


def names_json():
    result = models.OtherName.query.all()
    result_json = []
    for o_name in result:
        o = {
            "name": o_name.name,
            "university_id": o_name.university_id,
            "university_name": o_name.university.name
        }
        result_json.append(o)
    return jsonify(name=result_json)


def campus_json():
    result = models.UniversityHeadquarter.query.all()
    result_json = []
    for campus in result:
        c = {
            "name": campus.campus_name,
            "university_id": campus.university_id,
            "university_name": campus.university.name,
            "lat": campus.lat,
            "long": campus.long
        }
        result_json.append(c)
    return jsonify(campus=result_json)


def career_json():
    result = models.Career.query.all()
    result_json = []
    for career in result:
        c = {
            "id": career.id,
            "name": career.name,
            "description": career.description,
            "type": career.type
        }
        result_json.append(c)
    return jsonify(career=result_json)


def careeratuniversity_json():
    result = models.CareerAtUniversity.query.all()
    result_json = []
    for careeru in result:
        cu = {
            "id": careeru.id,
            "name": careeru.career.name,
            "university": careeru.place.university.name,
            "campus": careeru.place.campus_name,
            "description": careeru.description,
            "type": careeru.career.type,
            "place_id": careeru.place.id,
            "university_id": careeru.place.university.id,
            "career_id": careeru.career.id
        }
        result_json.append(cu)
    return jsonify(career=result_json)


def select_university_data():
    result = models.University.query.all()
    data = []
    for university in result:
        dictionary = {
            "id": university.id,
            "name": university.name
        }
        data.append(dictionary)
    return data


def select_carrer_data():
    result = models.Career.query.all()
    data = []
    for career in result:
        dictionary = {
            "id": career.id,
            "name": career.name
        }
        data.append(dictionary)
    return data


def select_place_data():
    result = models.UniversityHeadquarter.query.all()
    data = []
    for place in result:
        dictionary = {
            "id": place.id,
            "university_and_campus": place.university.name+" sede "+place.campus_name,
            "name": place.campus_name,
            "university_id": place.university_id
        }
        data.append(dictionary)
    return data
#VIEWS

@app.route("/main")
@app.route('/index')
@app.route('/')
def hello():
    return render_template("main.html", config=config)


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
@app.route("/team")
def team():
    ret = ""
    for member in models.Team.query.all():
        ret += "<span>"+str(member.username)+"|"+str(member.age)+"</span><br/>"
    return ret

@app.route("/buscar", methods=['POST', 'GET'])
def buscar_index():
    if request.method == 'POST':
        url = "/buscar/"+request.form['search']
        return redirect(url)
    return render_template("search.html",title=config.AppName)

@app.route("/buscar_json", methods=['POST', 'GET'])
def search_json():
    if request.method == 'GET':
        result = db.session.query(models.OtherName).filter(models.OtherName.name.ilike("%"+request.args.get("search")+"%"))
        result_json = []
        for o_name in result:
            o = {
                "name": o_name.name,
                "university_id": o_name.university_id,
                "university_name": o_name.university.name
            }
            result_json.append(o)
        return jsonify(names=result_json)
@app.route("/buscar/<busqueda>")
def buscar(busqueda):
    result = search.search_for(busqueda)
    if(len(result)==1):
        if (isinstance(result[0],models.University)):
            return render_template("university.html",university = result[0])
        elif(isinstance(result[0],models.Career)):
            return render_template("career.html",career  = result[0])
    elif (isinstance(result[0],models.University) or isinstance(result[0],models.Career)):
        return render_template("results.html",result = result)
    elif (result[0]==0):
        result.__delitem__(0)
        ret =  "Quizas quiso decir: <a href='/buscar/"+result[0]+"'>"+ result[0]+ "</a>"
        result.__delitem__(0)
        for item in result:
                ret += " o <a href='/buscar/"+item+"'>"+ item+"</a>"
        return ret
    return "Lo sentimos, no se han encontrado resultados"
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
    return redirect(url_for("hello"))


@app.route("/admin")
def admin_link():
    if check_log():
        return check_log()
    else:
        return 'Building... while you can go to the <a href="/panel/add/university">Panel</a>'


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


@app.route("/panel/add/name", methods=['POST', 'GET'])
def panel_add_name():
    if check_log():
        return check_log()
    else:
        if request.method == 'POST':
            if request.form["name"] and request.form["id"]:
                try:
                    university = models.University.query.filter_by(id=request.form["id"]).first()
                    name = models.OtherName(request.form["name"], university)
                    db.session.add(name)
                    db.session.commit()
                    return render_template("form_result.html", success=True)
                except:
                    return render_template("form_result.html", error=True)
            else:
                return render_template("form_result.html", error=True)
        else:
            return render_template("form_name.html", data=select_university_data())


@app.route("/panel/add/campus", methods=['POST', 'GET'])
def panel_add_campus():
    if check_log():
        return check_log()
    else:
        if request.method == 'POST':
            if request.form["name"] and request.form["id"] and request.form["lat"] and request.form["long"]:
                try:
                    university = models.University.query.filter_by(id=request.form["id"]).first()
                    campus = models.UniversityHeadquarter(request.form["name"], float(request.form["lat"]),
                                                          float(request.form["long"]), university)
                    db.session.add(campus)
                    db.session.commit()
                    return render_template("form_result.html", success=True)
                except:
                    return render_template("form_result.html", error=True)
            else:
                return render_template("form_result.html", error=True)
        else:
            return render_template("form_campus.html", data=select_university_data())


@app.route("/panel/add/career", methods=['POST', 'GET'])
def panel_add_career():
    if check_log():
        return check_log()
    else:
        if request.method == 'POST':
            if request.form["name"] and request.form["description"] and request.form["type"]:
                try:
                    career = models.Career(request.form["name"].encode('utf-8'), request.form["type"],
                                           request.form["description"])
                    db.session.add(career)
                    db.session.commit()
                    return render_template("form_result.html", success=True)
                except:
                    return render_template("form_result.html", error=True)
            else:
                return render_template("form_result.html", error=True)
        else:
            return render_template("form_career.html")


@app.route("/panel/add/careeratuniversity", methods=['POST', 'GET'])
def panel_add_careeratuniversity():
    if check_log():
        return check_log()
    else:
        if request.method == 'POST':
            if request.form["place_id"] and request.form["career_id"] and request.form["description"]:
                try:
                    place = models.UniversityHeadquarter.query.filter_by(id=request.form["place_id"]).first()
                    career = models.Career.query.filter_by(id=request.form["career_id"]).first()
                    careeratuniversity = models.CareerAtUniversity(request.form["description"],
                                                                   place, career)
                    db.session.add(careeratuniversity)
                    db.session.commit()
                    return render_template("form_result.html", success=True)
                except:
                    return render_template("form_result.html", error=True)
            else:
                return render_template("form_result.html", error=True)
        else:
            return render_template("form_careeratuniversity.html", places=select_place_data(),
                                   careers=select_carrer_data())


@app.route("/list/university")
def list_university():
    return university_json()


@app.route("/list/name")
def list_names():
    return names_json()


@app.route("/list/campus")
def list_campus():
    return campus_json()


@app.route("/list/career")
def list_career():
    return career_json()


@app.route("/list/careeratuniversity")
def list_careeratuniversity():
    return careeratuniversity_json()


@app.route("/universities/<university>")
def universities_page(university):
    u = models.University.query.filter(models.University.name.contains(university)).all()
    #return str(len(u))
    if len(u) <= 0:
        return redirect(url_for("buscar_index"))
    else:
        return render_template("university.html", university=u[0])


@app.route("/test")
def test():
        return render_template("university.html",university=models.University.query.all()[2])