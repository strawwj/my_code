from app import db
from app import app
import pymysql
pymysql.install_as_MySQLdb()
from app.models import Student
db.create_all()
