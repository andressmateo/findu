from flask_restful import Resource
from flask import request
from sqlalchemy import func
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from app import models, api
import unicodedata


################ Util ###################

def flat_text(s):
    if isinstance(s, str):
        s = s.decode("utf-8")
    return (''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))).lower()

class unaccent(ReturnTypeFromArgs):
    pass

def search(question):
    question = flat_text(question)
    result = {}
    result['u'] = models.University.query.filter(unaccent(func.lower(models.University.name)).contains(question)).all()
    result['o'] = models.OtherName.query.filter(unaccent(func.lower(models.OtherName.name)).contains(question)).all()
    [result['u'].append(o.university) for o in result['o']]
    result['c'] = models.Career.query.filter(unaccent(func.lower(models.Career.name)).contains(question)).all()
    result['k'] = models.KnowledgeArea.query.filter(unaccent(func.lower(models.KnowledgeArea.name)).
                                                    contains(question)).all()
    result['h'] = models.UniversityHeadquarter.query.filter(unaccent(func.lower(models.UniversityHeadquarter.
                                                                                campus_name)).contains(question)).all()
    result['n'] = len(result['u'])+len(result['c'])+len(result['k'])+len(result['h'])
    return result


############# Api classes ###############

class ApiSearch(Resource):
    def get(self):
        if "question" in request.args or "token" in request.args:
            if not "token" in request.args:
                result = search(request.args.get('question'))
                if result['n'] != 0:
                    return {"status":"ok","universities":[u.dict()for u in result['u']],
                            "careers":[c.dict() for c in result['c']],'knowledgesAreas':[k.dict() for k in result['k']],
                            'headquarter':[h.dict() for h in result['h']]}
                else:
                    return {"status": "error","error":"No results"}
            else:
                token = request.args.get('token')
        else:
            return {"status": "error","error":"Not enough parameters"}


class ApiUniversity(Resource):
    def get(self):
        return
    def post(self):
        return

api.add_resource(ApiSearch, '/api/search', "/api/search/")
api.add_resource(ApiUniversity, '/api/universities')