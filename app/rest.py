from flask_restful import Resource
from flask import request
from sqlalchemy import func
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from app import models, api
import unicodedata

class ApiSearch(Resource):
    def get(self):
        if "question" in request.args:
            question = flat_text(request.args.get('question'))
            universities = models.University.query.filter(unaccent(func.lower(models.University.name)).
                                                          contains(question)).all()
            other = models.OtherName.query.filter(unaccent(func.lower(models.OtherName.name)).contains(question)).all()
            [universities.append(o.university) for o in other]
            careers = models.Career.query.filter(unaccent(func.lower(models.Career.name)).contains(question)).all()
            know = models.KnowledgeArea.query.filter(unaccent(func.lower(models.KnowledgeArea.name)).
                                                     contains(question)).all()
            return {"status":"ok","universities":[u.dict()for u in universities],"careers":[c.dict() for c in careers]}
        else:
            return {"status": "error","error":"Not enough parameters"}


def flat_text(s):
    if isinstance(s, str):
        s = s.decode("utf-8")
    return (''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))).lower()

class unaccent(ReturnTypeFromArgs):
    pass


class ApiUniversity(Resource):
    def get(self):
        return
    def post(self):
        return

api.add_resource(ApiSearch, '/api/search', "/api/search/")
api.add_resource(ApiUniversity, '/api/universities')