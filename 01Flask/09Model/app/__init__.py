from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#app.config['WTF_CSRF_ENABLE']=True   
app.config.from_object('config')#'config是个字典'
db = SQLAlchemy(app)
from . import views
