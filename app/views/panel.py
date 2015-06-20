from flask import Blueprint, request, render_template
from app import db, models, util
import json

mod = Blueprint('panel', __name__, url_prefix='/panel')
@mod.route("/")
def panel():
    return render_template("panel/base.html")

@mod.route("/list_university")
def list_university():
    universities = db.session.query(models.University).all()
    return render_template("panel/list/list_university.html", universities = universities)


@mod.route("/list_career")
def list_career():
    careers = db.session.query(models.Career).all()
    return render_template("panel/list/list_career.html", careers = careers)


@mod.route("/list_name")
def list_name():
    names = db.session.query(models.OtherName).all()
    return render_template("panel/list/list_name.html", names = names)


@mod.route("/list_campus")
def list_campus():
    campuses = db.session.query(models.UniversityHeadquarter).all()
    return render_template("panel/list/list_campus.html", campuses = campuses)

@mod.route("/list_knowledge_area")
def list_knowledge_area():
    knowledges = db.session.query(models.KnowledgeArea).all()
    return render_template("panel/list/list_knowledge_area.html", knowledges = knowledges)

#cat_university for career_at_university
@mod.route("/list_cat_university")
def list_cat_university():
    cats_university = db.session.query(models.CareerAtUniversity).all()
    return render_template("panel/list/list_cat_university.html", cats_university = cats_university)

@mod.route("/view_university/<university>")
def view_university(university):
    u = db.session.query(models.University).filter_by(id = university)
    universities = db.session.query(models.University).all()
    return render_template("panel/view/view_university.html",university=u[0], universities = universities)


@mod.route("/view_career/<career>")
def view_career(career):
    c = db.session.query(models.Career).filter_by(id = career)
    careers = db.session.query(models.Career).all()
    return render_template("panel/view/view_career.html",career=c[0], careers = careers)

@mod.route("/view_name/<name>")
def view_name(name):
    n = db.session.query(models.OtherName).filter_by(name = name)
    names = db.session.query(models.OtherName).all()
    return render_template("panel/view/view_name.html",name=n[0], names = names)


@mod.route("/view_campus/<campus>")
def view_campus(campus):
    n = db.session.query(models.UniversityHeadquarter).filter_by(id = campus)
    campuses = db.session.query(models.UniversityHeadquarter).all()
    return render_template("panel/view/view_campus.html",campus=n[0], campuses = campuses)


@mod.route("/view_cat_university/<cat_university>")
def view_cat_university(cat_university):
    n = db.session.query(models.CareerAtUniversity).filter_by(id = cat_university)
    cats_university = db.session.query(models.CareerAtUniversity).all()
    return render_template("panel/view/view_cat_university.html",cat_university=n[0], cats_university = cats_university)


@mod.route("/view_knowledge_area/<knowledge_area>")
def view_knowledge_area(knowledge_area):
    k = db.session.query(models.KnowledgeArea).filter_by(id = knowledge_area)
    knowledges = db.session.query(models.KnowledgeArea).all()
    return render_template("panel/view/view_knowledge_area.html",knowledge=k[0],  knowledges = knowledges)


@mod.route("/add_university", methods=['POST', 'GET'])
def add_university():
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
        return render_template("panel/form/form_university.html",universities=universities)

@mod.route("/add_career", methods=['POST', 'GET'])
def add_career():
    if request.args.get("method") == 'POST':
        try:
            k = json.loads(request.args.get("knowledges"))
            names = list(k)
            knowledges = db.session.query(models.KnowledgeArea).filter(models.KnowledgeArea.name.in_(names)).all()
            career = models.Career(request.args.get("name").encode('utf-8'), request.args.get("type"),
                                       request.args.get("description").encode('utf-8'),knowledges,
                                   request.args.get("icon"),request.args.get("background"))
            db.session.add(career)
            db.session.commit()
            return str(1)
        except:
            return str(0)
    else:
        knowledges = db.session.query(models.KnowledgeArea).all()
        careers = db.session.query(models.Career).all()
        return render_template("panel/form/form_career.html",careers=careers, knowledges = knowledges)


@mod.route("/add_name", methods=['POST', 'GET'])
def add_name():
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
        return render_template("panel/form/form_name.html",names=names,  data=util.select_university_data())


@mod.route("/add_campus", methods=['POST', 'GET'])
def add_campus():
    if request.args.get("method") == 'POST':

        university = models.University.query.filter_by(id=request.args.get("id")).first()
        campus = models.UniversityHeadquarter(request.args.get("name").encode('utf-8'), float(request.args.get("lat")),
                                                  float(request.args.get("long")), university)
        db.session.add(campus)
        db.session.commit()
        return str(1)

    else:
        campuses = db.session.query(models.UniversityHeadquarter).all()
        return render_template("panel/form/form_campus.html", campuses=campuses,  data=util.select_university_data())


@mod.route("/add_cat_university", methods=['POST', 'GET'])
def add_cat_university():
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
            cat_university = models.CareerAtUniversity(request.args.get("description").encode('utf-8'), university,
                                                       career, places)
            db.session.add(cat_university)
            db.session.commit()
            return str(1)
            #return str(career.name).encode('utf-8')
        #except Exception, e:
         #   return str(e)
    else:
        cats_university = db.session.query(models.CareerAtUniversity).all()
        return render_template("panel/form/form_cat_university.html",cats_university=cats_university,
                               places=util.select_place_data(), careers=util.select_career_data())

@mod.route("/add_knowledge_area", methods=['POST', 'GET'])
def add_knowledge_area():
    if request.args.get("method") == 'POST':
        k = models.KnowledgeArea(request.args.get("name").encode('utf-8'),request.args.get("definition").\
                                 encode('utf-8'))
        db.session.add(k)
        db.session.commit()
        return str(1)
    else:
        knowledges = db.session.query(models.KnowledgeArea).all()
        return render_template("panel/form/form_knowledge_area.html",knowledges=knowledges)


@mod.route("/edit_university/<university>")
def edit_university(university):
    u = db.session.query(models.University).filter_by(id = university)
    universities = db.session.query(models.University).all()
    return render_template("panel/edit/university.html",university=u[0], universities = universities)

@mod.route("/edit_university", methods=['POST', 'GET'])
def save_changes_university():
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


@mod.route("/edit_career/<career>")
def edit_career(career):
    u = db.session.query(models.Career).filter_by(id = career)
    careers = db.session.query(models.Career).all()
    knowledges = db.session.query(models.KnowledgeArea).all()
    return render_template("panel/edit/career.html",career=u[0], careers = careers, knowledges = knowledges)
    #return render_template("career.html",career=u[0], careers = careers)


@mod.route("/edit_career", methods=['POST', 'GET'])
def save_changes_career():
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


@mod.route("/edit_campus/<campus>")
def edit_campus(campus):
    u = db.session.query(models.UniversityHeadquarter).filter_by(id = campus)
    campuses = db.session.query(models.UniversityHeadquarter).all()
    return render_template("panel/edit/campus.html",campus=u[0], campuses = campuses, data=util.select_university_data())


@mod.route("/edit_campus", methods=['POST', 'GET'])
def save_changes_campus():
    try:
        models.UniversityHeadquarter.query.filter_by(id=request.args.get("id")).\
        update({models.UniversityHeadquarter.campus_name: request.args.get("name").encode('utf-8'),
                models.UniversityHeadquarter.lat: float(request.args.get("lat")),
                models.UniversityHeadquarter.long: float(request.args.get("long"))}, synchronize_session=False)
        db.session.commit()
        return str(1)
    except:
        return str(0)


@mod.route("/edit_cat_university/<cat_university>")
def edit_cat_university(cat_university):
    u = db.session.query(models.CareerAtUniversity).filter_by(id = cat_university)[0]
    cats_university = db.session.query(models.CareerAtUniversity).all()
    return render_template("panel/edit/catUniversity.html",cat_university=u[0],cats_university = cats_university,
                           places=util.select_place_data(), careers=util.select_career_data())


@mod.route("/edit_cat_university", methods=['POST', 'GET'])
def save_changes_cat_university():
    try:
        models.CareerAtUniversity.query.filter_by(id=request.args.get("id")).\
        update({models.CareerAtUniversity.description: request.args.get("description").encode('utf-8')},
               synchronize_session=False)
        db.session.commit()
        return str(1)
    except:
        return str(0)


@mod.route("/edit_knowledge_area/<knowledge_area>")
def edit_knowledge_area(knowledge_area):
    k = db.session.query(models.KnowledgeArea).filter_by(id = knowledge_area)
    knowledges = db.session.query(models.KnowledgeArea).all()
    return render_template("panel/edit/knowledgeArea.html",knowledge=k[0],knowledges = knowledges)


@mod.route("/edit_knowledge_area", methods=['POST', 'GET'])
def save_changes_knowledge_area():
    try:
        models.KnowledgeArea.query.filter_by(id=request.args.get("id")).\
        update({models.KnowledgeArea.name: request.args.get("name").encode('utf-8'),
                models.KnowledgeArea.definition : request.args.get("definition").encode('utf-8')},
               synchronize_session=False)
        db.session.commit()
        return str(1)
    except:
        return str(0)

### Delete ###

@mod.route("/delete_university", methods=['POST', 'GET'])
def panel_delete_university():
    try:
        models.OtherName.query.filter_by(university_id=request.args.get("id")).delete(synchronize_session=False)
        uh = models.UniversityHeadquarter.query.filter_by(university_id=request.args.get("id"))
        for uh_id in uh:
            models.CareerAtUniversity.query.filter_by(place_id=uh_id.id).delete(synchronize_session=False)
        models.UniversityHeadquarter.query.filter_by(university_id=request.args.get("id")).\
            delete(synchronize_session=False)
        models.University.query.filter_by(id=request.args.get("id")).delete(synchronize_session=False)
        db.session.commit()
        return str(1)
    except:
        return str(0)


@mod.route("/delete_career", methods=['POST', 'GET'])
def panel_delete_career():
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


@mod.route("/delete_name", methods=['POST', 'GET'])
def panel_delete_name():
    try:
        db.session.query(models.OtherName).filter(models.OtherName.name.ilike(request.args.get("name")+"")).\
            delete(synchronize_session=False)
        db.session.commit()
        return str(1)
    except:
        return str(0)

@mod.route("/delete_campus", methods=['POST', 'GET'])
def panel_delete_campus():
    try:
        models.CareerAtUniversity.query.filter_by(place_id=request.args.get("id")).delete(synchronize_session=False)
        models.UniversityHeadquarter.query.filter_by(id=request.args.get("id")).delete(synchronize_session=False)
        db.session.commit()
        return str(1)
    except:
        return str(0)


@mod.route("/delete_knowledge_area", methods=['POST', 'GET'])
def panel_delete_knowledge_area():
    try:
        k = models.KnowledgeArea.query.filter_by(id=request.args.get("id")).first()
        for c in k.careers:
            c.knowledge_areas.remove(k)
        models.KnowledgeArea.query.filter_by(id=request.args.get("id")).delete(synchronize_session=False)
        db.session.commit()
        return str(1)
    except:
        return str(0)


@mod.route("/delete_cat_university", methods=['POST', 'GET'])
def panel_delete_cat_university():
    try:
        models.CareerAtUniversity.query.filter_by(id=request.args.get("id")).delete(synchronize_session=False)
        db.session.commit()
        return str(1)
    except:
        return str(0)
