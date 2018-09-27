from flask import Flask
from flask_sqlalchemy import SQLAlchemy
sqlApp = Flask(__name__)
sqlApp.config.from_object('config')
db=SQLAlchemy(sqlApp)
