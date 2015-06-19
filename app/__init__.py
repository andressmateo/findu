from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.database["url"]
app.secret_key = config.secret_key
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


from app.views import functions
from app.views import index
from app.views import search
from app.views import panel
app.register_blueprint(index.mod)
app.register_blueprint(search.mod)
app.register_blueprint(panel.mod)

