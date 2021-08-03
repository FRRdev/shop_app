from flask import render_template,flash,url_for,redirect,request
from flask_login import current_user,login_user,login_required
from app import app,db
from app.models import Users
from app.forms import RegistrationForm


@app.route('/index')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html',title='Авторизация')

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        u = Users(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                  email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Поздравляем,вы новый пользователь!!!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Регистрация', form=form)

