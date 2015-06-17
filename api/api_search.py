# -*- coding: utf8 -*-
from app import app
from data import models
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from sqlalchemy import func
import unicodedata


@app.route("/api/search")
def contact():
    return "Search_Api"

#Don't Touch
class unaccent(ReturnTypeFromArgs):
    pass


def flat_text(s):
    if isinstance(s, str):
        s = s.decode("utf-8")
    return (''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))).lower()


def search(question):
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
    '''query = {
        "u": [],
        "c": [],
        "s": [],
        "o": [],
        "k": []
    }
    #"Universidades:"
    if param == "all" or param == "u":
        query["u"] = models.University.query.filter(unaccent(func.lower(models.University.name))==(question)).all()
    #"Carreras:"
    if param == "all" or param == "c":
        query["c"] = models.Career.query.filter(unaccent(func.lower(models.Career.name))==(question)).all()
    #"Sedes:"
    if param == "all" or param == "s":
        query["s"] = models.UniversityHeadquarter.query.filter(unaccent(func.lower(models.UniversityHeadquarter.campus_name)).contains(question)).all()
    #"OtherNames"
    if param == "all" or param == "u" or param == "o":
        query["o"] = models.OtherName.query.filter(unaccent(func.lower(models.OtherName.name)).contains(question)).all()
    return query#"OtherNames"
    if param == "all" or param == "k":
        query["k"] = models.KnowledgeArea.query.filter(unaccent(func.lower(models.KnowledgeArea.name))==(question)).all()
    return query'''
