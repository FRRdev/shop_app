from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, Length, EqualTo
from app.models import Users


class RegistrationForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email(message='Введите корректную почту')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите авроль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегестрироваться')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста используйте другое имя')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Эта почта уже занята')
