# -*- coding: utf8 -*-
from app import models, app, db
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from sqlalchemy import func
import unicodedata


#Don't Touch
class unaccent(ReturnTypeFromArgs):
    pass


def flat_text(s):
    if isinstance(s, str):
        s = s.decode("utf-8")
    return (''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))).lower()


def search(question, param="all"):
    question = flat_text(question)
    query = {
        "u": [],
        "c": [],
        "s": [],
        "o": []
    }
    #"Universidades:"
    if param == "all" or param == "u":
        query["u"] = models.University.query.filter(unaccent(func.lower(models.University.name)).contains(question)).all()
    #"Carreras:"
    if param == "all" or param == "c":
        query["c"] = models.Career.query.filter(unaccent(func.lower(models.Career.name)).contains(question)).all()
    #"Sedes:"
    if param == "all" or param == "s":
        query["s"] = models.UniversityHeadquarter.query.filter(unaccent(func.lower(models.UniversityHeadquarter.campus_name)).contains(question)).all()
    #"OtherNames"
    if param == "all" or param == "u" or param == "o":
        query["o"] = models.OtherName.query.filter(unaccent(func.lower(models.OtherName.name)).contains(question)).all()
    return query