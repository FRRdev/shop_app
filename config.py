import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ##### настройка Flask-Mail #####
    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    #MAIL_USE_TLS = True
    MAIL_USERNAME = 'mixail.critsyn@mail.ru'
    MAIL_PASSWORD = 'yourpass'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    POSTS_PER_PAGE = 3
    ADMINS = ['mixail.critsyn@mail.ru']

    #вывод кирилицы в api
    JSON_AS_ASCII = False

    SECURITY_PASSWORD_SALT = 'My-SALT'
    # URLs
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Включает регистрацию
    SECURITY_REGISTERABLE = True
    SECURITY_REGISTER_URL = "/register/"
    SECURITY_SEND_REGISTER_EMAIL = False

    # Включет сброс пароля
    SECURITY_RECOVERABLE = True
    SECURITY_RESET_URL = "/reset/"
    SECURITY_SEND_PASSWORD_RESET_EMAIL = True

    # Включает изменение пароля
    SECURITY_CHANGEABLE = True
    SECURITY_CHANGE_URL = "/change/"
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
        'postgresql://postgres:Zahita183@localhost/shop_app'


class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
			      'postgresql://postgres:Zahita183@localhost/shop_app'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
	'postgresql://postgres:Zahita183@localhost/shop_app'