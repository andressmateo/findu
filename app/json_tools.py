from flask import  jsonify
from app import app, db, models, search


def university_json():
    result = models.University.query.all()
    result_json = []
    for university in result:
        u = {
            "id": university.id,
            "name": university.name,
            "description": university.description,
            "logo": university.logo,
            "accredited": university.accredited,
            "name_url" : university.name.replace(' ','-'),
            "background": university.background,
            "type": university.type
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

def search_json(search):
        resultC = db.session.query(models.Career).filter(models.Career.name.ilike("%"+search+"%"))
        resultU = db.session.query(models.University).filter(models.University.name.ilike("%"+search+"%"))
        resultO = db.session.query(models.OtherName).filter(models.OtherName.name.ilike("%"+search+"%"))
        resultS = db.session.query(models.UniversityHeadquarter).filter(models.UniversityHeadquarter.
                                                                        campus_name.ilike("%"+search+"%"))
        resultK = db.session.query(models.KnowledgeArea).filter(models.KnowledgeArea.name.ilike("%"+search+"%"))

        result_json = []
        for o_name in resultC:
            o = {
                "name": o_name.name,
            }
            result_json.append(o)
        for o_name in resultU:
            o = {
                "name": o_name.name,
            }
            result_json.append(o)
        for o_name in resultO:
            o = {
                "name": o_name.name,
            }
            result_json.append(o)
        for o_name in resultS:
            o = {
                "name": o_name.campus_name,
            }
            result_json.append(o)
        for o_name in resultK:
            o = {
                "name": o_name.name,
            }
            result_json.append(o)
        return jsonify(names=result_json)


def knowledge_area_json(search=""):
    result = db.session.query(models.KnowledgeArea).filter(models.KnowledgeArea.name.ilike("%"+search+"%"))
    result_json = []
    for knowledge in result:
        cu = {
            "id": knowledge.id,
            "name": knowledge.name,
            "definition": knowledge.definition,
        }
        result_json.append(cu)
    return jsonify(knowledges=result_json)