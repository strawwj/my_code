class Config():
    UPLOADED_HEADIMAGE_DEST = '/tmp/'
    WTF_CSRF_ENABLE = True
    SECRET_KEY = 'IOT.STRAW.COM'

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'wj18333226501@163.com'
    MAIL_PASSWORD = 'wj042397'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@172.25.4.216/iot_db'


class TestConfig(Config):
    TEST = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@172.25.4.216/test_db'


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@172.25.4.216/product_db'


config = {
    'develop': DevelopConfig,
    'test': TestConfig,
    'product': ProductConfig,
    'default': DevelopConfig
}