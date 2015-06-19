"""
Debug esta por activado por defecto
-p para ver en produccion
"""
import sys
from app import app
try:
    if sys.argv[1]=="-d":
        print "Modo: Debug"
        app.run(host='0.0.0.0',debug=True)
    elif sys.argv[1]=="-p":
        app.run(host='0.0.0.0',debug=False)
    else:
        print "Modo: Debug"
        app.run(host='0.0.0.0',debug=True)
except IndexError:
    print "Modo: Debug"
    app.run(host='0.0.0.0',debug=True)