from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth


import config
app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.database["url"]
app.secret_key = config.secret_key
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
auth = HTTPBasicAuth()

#Models Imports
import models
#Views Imports
from app import views
from app import rest
from app.views import functions
from app.views import index
from app.views import search
from app.views import panel
app.register_blueprint(index.mod)
app.register_blueprint(search.mod)
app.register_blueprint(panel.mod)
#Api Imports
from api import authentication