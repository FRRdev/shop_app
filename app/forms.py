from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, Length, EqualTo
from app.models import Users


class LoginForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Никнейм',
                           validators=[DataRequired(), Length(min=4, message='Минимальная длина поля 4 символа')])
    first_name = StringField('Имя',
                             validators=[DataRequired(), Length(min=4, message='Минимальная длина поля 4 символа')])
    last_name = StringField('Фамилия',
                            validators=[DataRequired(), Length(min=4, message='Минимальная длина поля 4 символа')])
    email = StringField('Почта', validators=[DataRequired(), Email(message='Введите корректную почту')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите авроль', validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегестрироваться')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста используйте другое имя')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Эта почта уже занята')


class CommentForm(FlaskForm):
    text = TextAreaField('Отзыв')
    submit = SubmitField('Отправить')

