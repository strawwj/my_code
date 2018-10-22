from app import create_app
from app import db
from flask_script import Manager, Shell
import pymysql
from flask_migrate import MigrateCommand, Migrate
from app.models import Role
pymysql.install_as_MySQLdb()

app = create_app('develop')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


def make_context():
    return dict(db=db)


manager.add_command('shell', Shell(make_context=make_context))


@manager.command
def test():
    import unittest
    t = unittest.TestLoader()
    t = t.discover('tests')
    unittest.TextTestRunner().run(t)


@manager.command
def init():
    Role.create_roles()


manager.run()
