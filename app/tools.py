from flask import session, redirect, url_for
from app import models

def check_log():
    if not session["logged"]:
        return redirect(url_for("login"))

def select_university_data():
    result = models.University.query.all()
    data = []
    for university in result:
        dictionary = {
            "id": university.id,
            "name": university.name
        }
        data.append(dictionary)
    return data

def select_career_data():
    result = models.Career.query.all()
    data = []
    for career in result:
        dictionary = {
            "id": career.id,
            "name": career.name
        }
        data.append(dictionary)
    return data


def select_place_data():
    result = models.UniversityHeadquarter.query.all()
    data = []
    for place in result:
        dictionary = {
            "id": place.id,
            "university_and_campus": place.university.name+" sede "+place.campus_name,
            "name": place.campus_name,
            "university_id": place.university_id
        }
        data.append(dictionary)
    return data