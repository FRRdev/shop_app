from flask import Flask
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DevelopementConfig
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(DevelopementConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
bootstrap = Bootstrap(app)
mail = Mail(app)
from app.admin.routes import admin_bp
from app.api import bp as api_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes, models, errors
