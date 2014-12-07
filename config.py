# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

BD_URL = "postgres://pautuijerpsjfe:SGKi84ubN5G8SJjtVbHKV47H2i@ec2-54-243-48-204.compute-1.amazonaws.com:5432/degiqggq043543"
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
#WHOOSH_BASE = os.path.join(basedir, 'search.db')
SQLALCHEMY_DATABASE_URI = BD_URL


#OTHER ONES
APP_SETTINGS="config.StagingConfig"
#APP DATA
AppName = "Project Athene"


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