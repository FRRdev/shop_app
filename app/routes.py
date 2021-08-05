from flask import render_template,flash,url_for,redirect,request
from flask_login import current_user,login_user,login_required,logout_user
from app import app,db
from app.models import Users
from app.forms import RegistrationForm,LoginForm

@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    return render_template('index.html',form1=form)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form1 = LoginForm()
    form2 = RegistrationForm()
    if form2.validate_on_submit():
        u = Users(username=form2.username.data, first_name=form2.first_name.data, last_name=form2.last_name.data,
                  email=form2.email.data)
        u.set_password(form2.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Поздравляем,вы новый пользователь!!!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Регистрация', form2=form2,form1=form1)

@app.route('/login',methods=['GET','POST'])
def login():
    form1 = LoginForm()
    if form1.validate_on_submit():
        user = Users.query.filter_by(username=form1.username.data).first()
        if user is None or not user.check_password(form1.password.data):
            flash('Неправильный ник или пароль')
            return render_template('index.html', form1=form1)
        login_user(user, remember=form1.remember_me.data)
        return redirect(url_for('index'))
    return render_template('index.html', form1=form1)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))