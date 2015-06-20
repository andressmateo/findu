from flask_restful import Resource, Api
from flask import request
from app import db, api

#Token
class ApiSearch(Resource):
    def get(self, question=None):
        def search(question, type='a'):
            question = flat_text(question)
            query = {
                "result": [],
                "associated": [],
            }

            u = models.University.query.filter(unaccent(func.lower(models.University.name))==(question)).all()
            if (u):
                query["result"] = u[0]
            c = models.Career.query.filter(unaccent(func.lower(models.Career.name))==(question)).all()
            if (c):
                query["result"] = c[0]
            k = models.KnowledgeArea.query.filter(unaccent(func.lower(models.KnowledgeArea.name)).contains(question)).all()
            if (k):
                query["result"] = k[0]
            return query
        return {"status": "OK"}





class ApiUniversity(Resource):
    def get(self):
        return
    def post(self):
        return

api.add_resource(ApiSearch, '/api/search', "/api/search/")
api.add_resource(ApiUniversity, '/api/universities')