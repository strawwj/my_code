from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

# 权限代表的网站的功能


class Permission():
    ADD_DEVICE = 0x0001
    DELETE_DEVICE = 0x0002
    EDIT_DEVICE = 0x0004
    ADD_SENSOR = 0x0008
    DELETE_SENSOR = 0x0010
    EDIT_SENSOR = 0x0020

    ADD_USER = 0x0040
    DELETE_USER = 0x0080
    EDIT_USER = 0x0100


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    private = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    about_me = db.Column(db.Text)
    password_hash = db.Column(db.String(128))
    register_time = db.Column(db.DateTime, default=datetime.now)
    access_time = db.Column(db.DateTime, default=datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))
    API_KEY = db.Column(db.String(256))
    location = db.Column(db.String(64))
    # 反向关系
    devices = db.relationship('Device', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    news = db.relationship('News', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def generate_confirmed_token(self):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'], expires_in=1200)
        token = s.dumps({'id': self.id})
        return token

    def get_api_token(self):
        return self.API_KEY

    def generate_api_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], 10*365*24*60*60)
        self.API_KEY = s.dumps({'id': self.id})
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_api_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        if 'id' not in data.keys():
            return None
        return User.query.filter_by(id=data['id']).first()

    def confirm(self, token):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'])
        try:
            d = s.loads(token)
        except:
            return False
        if d.get('id') == self.id:
            self.confirmed = True
            db.session.add(self)
            db.session.commit()
            return True
        return False

    # 构建属性
    @property
    def password(self):
        raise AttributeError('密码不能读取')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission):
        return self.role.permissions & permission == permission

    def is_admin(self):
        return self.has_permission(0xffff)

    def is_common_user(self):
        return self.has_permission(0x0001 | 0x0002 | 0x0004 | 0x0008 | 0x0010 | 0x0020)

    def flush_access_time(self):
        self.access_time = datetime.now()
        db.session.add(self)
        db.session.commit()


from flask_login import AnonymousUserMixin


class AnonymousUser(AnonymousUserMixin):
    name = '游客'

    def has_permission(self,permission):
        return False

    def is_admin(self):
        return False

    def is_common_user(self):
        return False

    def flush_access_time(self):
        pass

from app import login_manager


@login_manager.user_loader
def user_load(id):
    return User.query.get(int(id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    permissions = db.Column(db.Integer)
    default = db.Column(db.Boolean, default=False)
    # 反向关系
    users = db.relationship('User', backref='role', lazy='dynamic', cascade='all, delete-orphan')

    @staticmethod
    def create_roles():
        roles = {
            'common_user': [Permission.ADD_DEVICE | Permission.DELETE_DEVICE | \
                    Permission.EDIT_DEVICE | Permission.ADD_SENSOR | \
                    Permission.DELETE_SENSOR | Permission.EDIT_SENSOR, True],
            'business_user': [Permission.EDIT_DEVICE | Permission.EDIT_SENSOR, False],
            'admin': [0xffff, False]
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role()
                role.name = r
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    describe = db.Column(db.Text)
    location = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    timestamp = db.Column(db.DateTime, default=datetime.now)
    # 反向关系
    sensors = db.relationship('Sensor', backref='device', lazy='dynamic', cascade='all, delete-orphan')

    def to_json(self):
        json_data = {
            'id': self.id,
            'name': self.name,
            'user': self.user.name,
            'timestamp': self.timestamp
        }
        return json_data


class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    describe = db.Column(db.Text)
    unit = db.Column(db.String(128))
    max = db.Column(db.Float, default=1.0)
    min = db.Column(db.Float, default=1.0)
    access_data = db.Column(db.Float, default=0)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id', ondelete='CASCADE'))
    timestamp = db.Column(db.DateTime, default=datetime.now)
    # 反向关系
    datas = db.relationship('Data', backref='sensor', lazy='dynamic', cascade='all, delete-orphan')
    alters = db.relationship('Alert', backref='sensor', lazy='dynamic', cascade='all, delete-orphan' )

    def to_json(self):
        json_data = {
            'id': self.id,
            'name': self.name,
            'describe': self.describe,
            'device': self.device.name,
            'max': self.max,
            'min': self.min,
            # 'datas': self.datas,
            'unit': self.unit,
            'timestamp': self.timestamp
        }
        return json_data


class Data(db.Model):
    __tablename__ = 'datas'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id', ondelete='CASCADE'))
    # 反向关系
    alters = db.relationship('Alert', backref='data', lazy='dynamic', cascade='all, delete-orphan' )

    def to_json(self):
        json_data = {
            'id': self.id,
            'data': self.data,
            'timestamp': self.timestamp,
            'sensor': self.sensor.name
        }
        return json_data


class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    data_id = db.Column(db.Integer, db.ForeignKey('datas.id', ondelete='CASCADE'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id', ondelete='CASCADE'))
    current_max = db.Column(db.Float)
    current_min = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    reason = db.Column(db.String(128))