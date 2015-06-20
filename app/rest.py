from flask_restful import Resource, Api
from flask import request
from app import models, api
import unicodedata


class ApiSearch(Resource):
    def get(self):
        if "question" in request.args:
            question = request.args.get('question')
            universities = models.University.query.filter(models.University.name.ilike("%"+question+"%")).all()
            other = models.OtherName.query.filter(models.OtherName.name.ilike(question)).all()
            for o in other:
                universities.add(o)
            careers = models.Career.query.filter(models.Career.name.ilike('%'+question+'%')).all()
            know = models.KnowledgeArea.query.filter(models.KnowledgeArea.name.ilike(question)).all()
            return {"status":"ok","universities":question}
        else:
            return {"status": "error","error":"Not enough parameters"}





class ApiUniversity(Resource):
    def get(self):
        return
    def post(self):
        return

api.add_resource(ApiSearch, '/api/search', "/api/search/")
api.add_resource(ApiUniversity, '/api/universities')