import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return 'Deployment...'

#Ejemplo de Obtener datos de una Ruta
@app.route("/w/<name>")
def helname(name):
    return "Hello {}!".format(name)
if __name__ == "__main__":
    app.run(debug=True)