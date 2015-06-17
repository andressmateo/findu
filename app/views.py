# -*- coding: utf-8 -*-
# -*- coding: latin-1 -*-
from flask import render_template, redirect, session, url_for, request, json
from app import app, db, models, search, template_global, tools, json_answers
import config
import random

@app.route("/main")
@app.route('/index')
@app.route('/')
def hello():
    return render_template("main.html", config=config)


@app.route("/404")
@app.errorhandler(404)
def not_found(error=""):
    print error
    return render_template("404.html")


@app.errorhandler(500)
def not_found(error):
    print error
    return render_template("404.html")


@app.route("/buscar", methods=['POST', 'GET'])
def buscar_index():
    if request.method == 'POST':
        url = "/buscar/"+request.form['search']
        return redirect(url)
    return render_template("search.html", title=config.AppName)


@app.route("/buscar/<busqueda>")
def buscar(busqueda):
    query = search.search(busqueda)
    '''repeated_one = set(query["u"]).intersection(set([x.university for x in query["o"]]))
    query["o"] = list(set([x.university for x in query["o"]]).difference(repeated_one))
    repeated_two = set(query["k"]).intersection(set([x.name for x in query["c"]]))
    query["k"] = list(set([x.name for x in query["c"]]).difference(repeated_two))
    query["word"] = busqueda'''
    return render_template("search_list.html", items=query)

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
    if tools.check_log():
        return tools.check_log()
    else:
        return render_template("panel_base.html")

######### Panel ##########
@app.route("/panel")
def panel():
    if tools.check_log():
        return tools.check_log()
    else:
        return render_template("panel_base.html")


@app.route("/panel/list_university")
def list_university():
    if tools.check_log():
        return tools.check_log()
    else:
        universities = db.session.query(models.University).all()
        return render_template("list_university.html", universities = universities)


@app.route("/panel/list_career")
def list_career():
    if tools.check_log():
        return tools.check_log()
    else:
        careers = db.session.query(models.Career).all()
        return render_template("list_career.html", careers = careers)


@app.route("/panel/list_name")
def list_name():
    if tools.check_log():
        return tools.check_log()
    else:
        names = db.session.query(models.OtherName).all()
        return render_template("list_name.html", names = names)


@app.route("/panel/list_campus")
def list_campus():
    if tools.check_log():
        return tools.check_log()
    else:
        campuses = db.session.query(models.UniversityHeadquarter).all()
        return render_template("list_campus.html", campuses = campuses)

@app.route("/panel/list_knowledge_area")
def list_knowledge_area():
    if tools.check_log():
        return tools.check_log()
    else:
        knowledges = db.session.query(models.KnowledgeArea).all()
        return render_template("list_knowledge_area.html", knowledges = knowledges)

#cat_university for career_at_university
@app.route("/panel/list_cat_university")
def list_cat_university():
    if tools.check_log():
        return tools.check_log()
    else:
        cats_university = db.session.query(models.CareerAtUniversity).all()
        return render_template("list_cat_university.html", cats_university = cats_university)

@app.route("/panel/view_university/<university>")
def view_university(university):
    if tools.check_log():
        return tools.check_log()
    else:
        u = db.session.query(models.University).filter_by(id = university)
        universities = db.session.query(models.University).all()
        return render_template("view_university.html",university=u[0], universities = universities)


@app.route("/panel/view_career/<career>")
def view_career(career):
    if tools.check_log():
        return tools.check_log()
    else:
        c = db.session.query(models.Career).filter_by(id = career)
        careers = db.session.query(models.Career).all()
        return render_template("view_career.html",career=c[0], careers = careers)


@app.route("/panel/view_name/<name>")
def view_name(name):
    if tools.check_log():
        return tools.check_log()
    else:
        n = db.session.query(models.OtherName).filter_by(name = name)
        names = db.session.query(models.OtherName).all()
        return render_template("view_name.html",name=n[0], names = names)


@app.route("/panel/view_campus/<campus>")
def view_campus(campus):
    if tools.check_log():
        return tools.check_log()
    else:
        n = db.session.query(models.UniversityHeadquarter).filter_by(id = campus)
        campuses = db.session.query(models.UniversityHeadquarter).all()
        return render_template("view_campus.html",campus=n[0], campuses = campuses)


@app.route("/panel/view_cat_university/<cat_university>")
def view_cat_university(cat_university):
    if tools.check_log():
        return tools.check_log()
    else:
        n = db.session.query(models.CareerAtUniversity).filter_by(id = cat_university)
        cats_university = db.session.query(models.CareerAtUniversity).all()
        return render_template("view_cat_university.html",cat_university=n[0], cats_university = cats_university)


@app.route("/panel/view_knowledge_area/<knowledge_area>")
def view_knowledge_area(knowledge_area):
    if tools.check_log():
        return tools.check_log()
    else:
        k = db.session.query(models.KnowledgeArea).filter_by(id = knowledge_area)
        knowledges = db.session.query(models.KnowledgeArea).all()
        return render_template("view_knowledge_area.html",knowledge=k[0],  knowledges = knowledges)


########### Panel CRUD ##############

### Add ###

@app.route("/panel/add_university", methods=['POST', 'GET'])
def add_university():
    if tools.check_log():
        return tools.check_log()
    else:
        if request.args.get("method") == 'POST':
            try:
                name = request.args.get("name")
                description = request.args.get("description")
                logo = request.args.get("logo")
                type = request.args.get("type")
                motto = request.args.get("motto")
                if (motto!=None):
                    motto = motto.encode('utf-8')
                established = request.args.get("established")
                principal = request.args.get("principal")
                if(principal!=None):
                    principal = principal.encode('utf-8')
                students = request.args.get("students")
                web = request.args.get("web")
                background = request.args.get("background")
                address = request.args.get("address")
                accredited = request.args.get("accredited")
                if(accredited==None):
                    accredited = False
                facebook = request.args.get("facebook")
                twitter = request.args.get("twitter")

                if(name==None or description==None or logo ==None):
                    return str(0)

                university = models.University(name.encode('utf-8'),description.encode('utf-8'),logo, background,
                                               motto, established, type, principal, students, web,address,
                                               accredited, facebook, twitter)
                db.session.add(university)
                db.session.commit()
                return str(1)
            except:
                return str(0)
        else:
            universities = db.session.query(models.University).all()
            return render_template("form_university.html",universities=universities)


@app.route("/panel/add_career", methods=['POST', 'GET'])
def add_career():
    if tools.check_log():
        return tools.check_log()
    else:
        if request.args.get("method") == 'POST':
            try:
                k = json.loads(request.args.get("knowledges"))
                names = list(k)
                knowledges = db.session.query(models.KnowledgeArea).filter(models.KnowledgeArea.name.in_(names)).all()
                career = models.Career(request.args.get("name").encode('utf-8'), request.args.get("type"),
                                           request.args.get("description").encode('utf-8'),knowledges,request.args.get("icon"),request.args.get("background"))
                db.session.add(career)
                db.session.commit()
                return str(1)
            except:
                return str(0)
        else:
            knowledges = db.session.query(models.KnowledgeArea).all()
            careers = db.session.query(models.Career).all()
            return render_template("form_career.html",careers=careers, knowledges = knowledges)


@app.route("/panel/add_name", methods=['POST', 'GET'])
def add_name():
    if tools.check_log():
        return tools.check_log()
    else:
        if request.args.get("method") == 'POST':
            try:
                university = models.University.query.filter_by(id=request.args.get("university")).first()
                name = models.OtherName(request.args.get("name").encode('utf-8'), university)
                db.session.add(name)
                db.session.commit()
                return str(1)
            except:
                return str(0)
        else:
            names = db.session.query(models.OtherName).all()
            return render_template("form_name.html",names=names,  data=tools.select_university_data())


@app.route("/panel/add_campus", methods=['POST', 'GET'])
def add_campus():
    if tools.check_log():
        return tools.check_log()
    else:
        if request.args.get("method") == 'POST':

            university = models.University.query.filter_by(id=request.args.get("id")).first()
            campus = models.UniversityHeadquarter(request.args.get("name").encode('utf-8'), float(request.args.get("lat")),
                                                      float(request.args.get("long")), university)
            db.session.add(campus)
            db.session.commit()
            return str(1)

        else:
            campuses = db.session.query(models.UniversityHeadquarter).all()
            return render_template("form_campus.html", campuses=campuses,  data=tools.select_university_data())


@app.route("/panel/add_cat_university", methods=['POST', 'GET'])
def add_cat_university():
    if tools.check_log():
        return tools.check_log()
    else:
        if request.args.get("action") == 'add':
           # try:
                p = json.loads(request.args.get("places"))
                places_id = list(p)
                #for x in places_id:
                #    places.append(models.UniversityHeadquarter.query.filter_by(id=x).first())
                places = models.UniversityHeadquarter.query.filter(models.UniversityHeadquarter.id.in_(places_id)).all()
                career = models.Career.query.filter_by(id=request.args.get("career_id")).first()
                #place.university.name = place.university.name.encode('utf-8')
                career.name = career.name.encode('utf-8')
                career.description = career.description.encode('utf-8')
                #place.university.description = place.university.description.encode('utf-8')
                university = models.University.query.filter_by(id=request.args.get("university_id"))[0]
                cat_university = models.CareerAtUniversity(request.args.get("description").encode('utf-8'), university, career, places)
                db.session.add(cat_university)
                db.session.commit()
                return str(1)
                #return str(career.name).encode('utf-8')
            #except Exception, e:
             #   return str(e)
        else:
            cats_university = db.session.query(models.CareerAtUniversity).all()
            return render_template("form_cat_university.html",cats_university=cats_university,places=tools.select_place_data(),
                                   careers=tools.select_career_data())

@app.route("/panel/add_knowledge_area", methods=['POST', 'GET'])
def add_knowledge_area():
    if tools.check_log():
        return tools.check_log()
    else:
        if request.args.get("method") == 'POST':
            k = models.KnowledgeArea(request.args.get("name").encode('utf-8'),request.args.get("definition").encode('utf-8'))
            db.session.add(k)
            db.session.commit()
            return str(1)
        else:
            knowledges = db.session.query(models.KnowledgeArea).all()
            return render_template("form_knowledge_area.html",knowledges=knowledges)

### Edit ###

@app.route("/panel/edit_university/<university>")
def edit_university(university):
    if tools.check_log():
        return tools.check_log()
    else:
        u = db.session.query(models.University).filter_by(id = university)
        universities = db.session.query(models.University).all()
        return render_template("edit_university.html",university=u[0], universities = universities)


@app.route("/panel/edit_university", methods=['POST', 'GET'])
def save_changes_university():
    if tools.check_log():
        return tools.check_log()
    else:
        try:
            name = request.args.get("name")
            description = request.args.get("description")
            logo = request.args.get("logo")
            type = request.args.get("type")
            motto = request.args.get("motto")
            if (motto!=None):
                motto = motto.encode('utf-8')
            established = request.args.get("established")
            if(established == None or established == ''):
                established = -1
            principal = request.args.get("principal")
            if(principal!=None):
                principal = principal.encode('utf-8')
            students = request.args.get("students")
            if (students == None or students == ''):
                students = -1
            web = request.args.get("web")
            background = request.args.get("background")
            address = request.args.get("address")
            accredited = request.args.get("accredited")
            if(accredited==None):
                    accredited = False
            facebook = request.args.get("facebook")
            twitter = request.args.get("twitter")

            if(name==None or description==None or logo ==None):
                return str(0)

            models.University.query.filter_by(id=request.args.get("id")).\
            update({models.University.name: name, models.University.description: description,
                    models.University.logo: logo, models.University.type : type,
                    models.University.motto : motto, models.University.established : established,
                    models.University.principal : principal, models.University.students : students,
                    models.University.web_site : web, models.University.background : background,
                    models.University.address : address, models.University.accredited : accredited,
                    models.University.facebook : facebook, models.University.twitter : twitter}, synchronize_session=False)
            db.session.commit()
            return str(1)
        except:
            return str(0)


@app.route("/panel/edit_career/<career>")
def edit_career(career):
    if tools.check_log():
        return tools.check_log()
    else:
        u = db.session.query(models.Career).filter_by(id = career)
        careers = db.session.query(models.Career).all()
        knowledges = db.session.query(models.KnowledgeArea).all()
        return render_template("edit_career.html",career=u[0], careers = careers, knowledges = knowledges)
        #return render_template("edit_career.html",career=u[0], careers = careers)


@app.route("/panel/edit_career", methods=['POST', 'GET'])
def save_changes_career():
    if tools.check_log():
        return tools.check_log()
    else:
        try:
            k = json.loads(request.args.get("knowledges"))
            names = list(k)
            c = models.Career.query.filter_by(id=request.args.get("id")).first()
            while(len(c.knowledge_areas)!=0):
                for kw in c.knowledge_areas:
                    c.knowledge_areas.remove(kw)
            knowledges = db.session.query(models.KnowledgeArea).filter(models.KnowledgeArea.name.in_(names)).all()
            for ka in knowledges:
                c.knowledge_areas.insert(len(c.knowledge_areas),ka)
            models.Career.query.filter_by(id=request.args.get("id")).\
            update({models.Career.name: request.args.get("name").encode('utf-8'),
                    models.Career.description: request.args.get("description").encode('utf-8'),
                    models.Career.type: request.args.get("type"), models.Career.icon: request.args.get("icon"),
                    models.Career.background: request.args.get("background")}, synchronize_session=False)
            db.session.commit()
            return str(1)
        except:
            return str(0)


@app.route("/panel/edit_campus/<campus>")
def edit_campus(campus):
    if tools.check_log():
        return tools.check_log()
    else:
        u = db.session.query(models.UniversityHeadquarter).filter_by(id = campus)
        campuses = db.session.query(models.UniversityHeadquarter).all()
        return render_template("edit_campus.html",campus=u[0], campuses = campuses, data=tools.select_university_data())


@app.route("/panel/edit_campus", methods=['POST', 'GET'])
def save_changes_campus():
    if tools.check_log():
        return tools.check_log()
    else:
        try:
            models.UniversityHeadquarter.query.filter_by(id=request.args.get("id")).\
            update({models.UniversityHeadquarter.campus_name: request.args.get("name").encode('utf-8'),
                    models.UniversityHeadquarter.lat: float(request.args.get("lat")),
                    models.UniversityHeadquarter.long: float(request.args.get("long"))}, synchronize_session=False)
            db.session.commit()
            return str(1)
        except:
            return str(0)


@app.route("/panel/edit_cat_university/<cat_university>")
def edit_cat_university(cat_university):
    if tools.check_log():
        return tools.check_log()
    else:
        u = db.session.query(models.CareerAtUniversity).filter_by(id = cat_university)[0]
        cats_university = db.session.query(models.CareerAtUniversity).all()
        return render_template("edit_cat_university.html",cat_university=u[0],cats_university = cats_university,
                               places=tools.select_place_data(), careers=tools.select_career_data())


@app.route("/panel/edit_cat_university", methods=['POST', 'GET'])
def save_changes_cat_university():
    if tools.check_log():
        return tools.check_log()
    else:
        try:
            models.CareerAtUniversity.query.filter_by(id=request.args.get("id")).\
            update({models.CareerAtUniversity.description: request.args.get("description").encode('utf-8')}, synchronize_session=False)
            db.session.commit()
            return str(1)
        except:
            return str(0)


@app.route("/panel/edit_knowledge_area/<knowledge_area>")
def edit_knowledge_area(knowledge_area):
    if tools.check_log():
        return tools.check_log()
    else:
        k = db.session.query(models.KnowledgeArea).filter_by(id = knowledge_area)
        knowledges = db.session.query(models.KnowledgeArea).all()
        return render_template("edit_knowledge_area.html",knowledge=k[0],knowledges = knowledges)


@app.route("/panel/edit_knowledge_area", methods=['POST', 'GET'])
def save_changes_knowledge_area():
    if tools.check_log():
        return tools.check_log()
    else:
        try:
            models.KnowledgeArea.query.filter_by(id=request.args.get("id")).\
            update({models.KnowledgeArea.name: request.args.get("name").encode('utf-8'),
                    models.KnowledgeArea.definition : request.args.get("definition").encode('utf-8')}, synchronize_session=False)
            db.session.commit()
            return str(1)
        except:
            return str(0)

### Delete ###

@app.route("/panel/delete_university", methods=['POST', 'GET'])
def panel_delete_university():
    if tools.check_log():
        return tools.check_log()
    else:
        try:
            models.OtherName.query.filter_by(university_id=request.args.get("id")).delete(synchronize_session=False)
            uh = models.UniversityHeadquarter.query.filter_by(university_id=request.args.get("id"))
            for uh_id in uh:
                models.CareerAtUniversity.query.filter_by(place_id=uh_id.id).delete(synchronize_session=False)
            models.UniversityHeadquarter.query.filter_by(university_id=request.args.get("id")).delete(synchronize_session=False)
            models.University.query.filter_by(id=request.args.get("id")).delete(synchronize_session=False)
            db.session.commit()
            return str(1)
        except:
            return str(0)


@app.route("/panel/delete_career", methods=['POST', 'GET'])
def panel_delete_career():
    if tools.check_log():
        return tools.check_log()
    else:
        try:
            c = models.Career.query.filter_by(id=request.args.get("id")).first()
            while(len(c.knowledge_areas)!=0):
                for kw in c.knowledge_areas:
                    c.knowledge_areas.remove(kw)
            models.CareerAtUniversity.query.filter_by(career_id=request.args.get("id")).delete(synchronize_session=False)
            models.Career.query.filter_by(id=request.args.get("id")).delete(synchronize_session=False)
            db.session.commit()
            return str(1)
        except:
            return str(0)


@app.route("/panel/delete_name", methods=['POST', 'GET'])
def panel_delete_name():
    if tools.check_log():
        return tools.check_log()
    else:
        try:
            db.session.query(models.OtherName).filter(models.OtherName.name.ilike(request.args.get("name")+"")).\
                delete(synchronize_session=False)
            db.session.commit()
            return str(1)
        except:
            return str(0)

@app.route("/panel/delete_campus", methods=['POST', 'GET'])
def panel_delete_campus():
    if tools.check_log():
        return tools.check_log()
    else:
        try:
            models.CareerAtUniversity.query.filter_by(place_id=request.args.get("id")).delete(synchronize_session=False)
            models.UniversityHeadquarter.query.filter_by(id=request.args.get("id")).delete(synchronize_session=False)
            db.session.commit()
            return str(1)
        except:
            return str(0)


@app.route("/panel/delete_knowledge_area", methods=['POST', 'GET'])
def panel_delete_knowledge_area():
    if tools.check_log():
        return tools.check_log()
    else:
        try:
            k = models.KnowledgeArea.query.filter_by(id=request.args.get("id")).first()
            for c in k.careers:
                c.knowledge_areas.remove(k)
            models.KnowledgeArea.query.filter_by(id=request.args.get("id")).delete(synchronize_session=False)
            db.session.commit()
            return str(1)
        except:
            return str(0)


@app.route("/panel/delete_cat_university", methods=['POST', 'GET'])
def panel_delete_cat_university():
    if tools.check_log():
        return tools.check_log()
    else:
        try:
            models.CareerAtUniversity.query.filter_by(id=request.args.get("id")).delete(synchronize_session=False)
            db.session.commit()
            return str(1)
        except:
            return str(0)

####################################################################

@app.route("/universidades")
def universities():
    retvar = models.University.query.all()
    random.shuffle(retvar)
    return render_template("universities.html", universities=retvar)


@app.route("/carreras")
def careers():
    retvar = models.Career.query.all()
    random.shuffle(retvar)
    return render_template("careers.html", careers=retvar)


@app.route("/universidades/<university>")
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
        return render_template("university.html", university=u[0])


@app.route("/carreras/<career>")
def careers_page(career):
    if " " in career:
        career = career.replace("-", " ")
        return redirect(url_for("buscar", busqueda=career))
    career = career.replace("-", " ")
    c = models.Career.query.filter_by(name=career).all()
    if len(c) <= 0:
        return redirect(url_for("buscar", busqueda=career))
    else:
        return render_template("career.html", career=c[0])


@app.route("/universidades/<university>/carreras/<career>")
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
    return render_template("career_at_university.html", careers=r)


@app.route("/universidades/<university>/sedes/<campus>")
def campus_page(university, campus):
    if " " in university or " " in campus:
        university = university.replace("-", " ")
        return redirect(url_for("buscar", busqueda=university))
    university = university.replace("-", " ")
    campus = campus.replace("-", " ")
    c = models.UniversityHeadquarter.query.filter_by(campus_name=campus).all()
    for campus in c:
        if campus.university.name == university:
            return render_template("campus.html", campus=campus)
    return redirect(url_for("404"))
