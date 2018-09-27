from app import app
from flask_script import Shell,Manager
import pymysql
pymysql.install_as_MySQLdb()
from app import db
from app.models import Student,Teacher
from flask_migrate import Migrate,MigrateCommand
migrate = Migrate(app,db)
manager = Manager(app)
def make_context():
	return dict(a=app,Student=Student,t=Teacher,d = db)
manager.add_command('shell',Shell(make_context=make_context))
manager.add_command('db',MigrateCommand)
manager.run()
#db.create_all()
#app.run(debug=True)
