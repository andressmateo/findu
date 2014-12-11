# -*- coding: utf8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

BD_URL = "postgres://pautuijerpsjfe:SGKi84ubN5G8SJjtVbHKV47H2i@ec2-54-243-48-204.compute-1.amazonaws.com:5432/degiqggq043543"
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# WHOOSH_BASE = os.path.join(basedir, 'search.db')
SQLALCHEMY_DATABASE_URI = BD_URL


# OTHER ONES
APP_SETTINGS = "config.StagingConfig"
#APP DATA
AppName = "Project Athene"
Team = "Atares"
State = "Alpha"
V = "0.0.1"
description = "En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor. Una olla de algo más vaca que carnero, salpicón las más noches, duelos y quebrantos los sábados, lantejas los viernes, algún palomino de añadidura los domingos, consumían las tres partes de su hacienda."
secretKey = "¿ah?"
adminUser = "admin"
adminPass = "123581321"

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = BD_URL


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True