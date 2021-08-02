from flask import render_template,flash
from flask_login import current_user,login_user,login_required
from app import app,db
from app.models import User


@app.route('/index')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html',title='Авторизация')