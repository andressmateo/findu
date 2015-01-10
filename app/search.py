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

"""
def levenshtein_distance(str1, str2):
  d=dict()
  for i in range(len(str1)+1):
     d[i]=dict()
     d[i][0]=i
  for i in range(len(str2)+1):
     d[0][i] = i
  for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
  return d[len(str1)][len(str2)]
"""