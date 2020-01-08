import os
from app import create_app, db
from app.models import Users, Roles, Permission
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Users=Users, Roles=Roles, Permission=Permission)

if __name__ == '__main__':
    manager.run()
