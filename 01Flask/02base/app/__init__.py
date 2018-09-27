from flask import Flask

app = Flask(__name__)

from . import views  #.为当前包下

