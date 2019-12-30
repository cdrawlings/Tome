import os
base = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'open sesame'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    APP_MAIL_SUBJECT_PREFIX = '[Adventures Tome]'
    APP_MAIL_SENDER = 'Adventures Tome Admin <dev@rawlings.site>'
    APP_ADMIN = 'c.d.rawlings@gmail.com'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.fatcow.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'dev@rawlings.site'
    MAIL_PASSWORD = 'Test1Test'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rawlings:1234@localhost:8889/tomeDB'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rawlings:1234@localhost:8889/tomeDB'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rawlings:1234@localhost:8889/tomeDB'

config = {
    'development': DevelopmentConfig,
    'testing':  TestingConfig,
    'production':  ProductionConfig,

    'default': DevelopmentConfig


}