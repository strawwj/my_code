from flask_mail import Mail, Message
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_moment import Moment
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
# login_manager通过操作session来控制用户的登录状态
# 通过对session的判断来决定用户能够访问的视图函数
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

moment = Moment()
mail = Mail()
db = SQLAlchemy()

from app.models import AnonymousUser
login_manager.anonymous_user = AnonymousUser
# 创建app的函数

# uploadset = UploadSet('headImage', IMAGES)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    # configure_uploads(app, uploadset)
    # patch_request_class(app, 32*1024*1024)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .manager import manager as manager_blueprint
    app.register_blueprint(manager_blueprint, url_prefix='/manager')

    from .api1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/1_0')

    return app


