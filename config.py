import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # #验证
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # #邮箱
    FLASKY_MAIL_SUBJECT_PERFIX = '[Flasky]'
    FLASK_MAIL_SENDER = 'Flasky Admin  <1487759857@qq.com>'
    FLASK_ADMIN = os.environ.get('FLASKY_ADMIN') or '2581716503@qq.com'
    # #数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = '1487759857@qq.com'
    MAIL_PASSWORD = 'bdflslmgfrhrfghb'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
