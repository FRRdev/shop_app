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
from app.admin.routes import admin_bp

app.register_blueprint(admin_bp, url_prefix='/admin')

from app import routes, models, errors
