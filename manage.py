#MIGRACIONES Y OTRAS CON LA BD

from app import app, db, manager, migrate
if __name__ == '__main__':
    manager.run()
