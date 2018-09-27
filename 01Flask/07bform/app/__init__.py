from flask import Flask
app = Flask(__name__)
#加载配置
app.config.from_object('config')
from . import views
