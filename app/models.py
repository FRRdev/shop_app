import re

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_security import RoleMixin
import os
from config import app_dir


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


cart_to_product = db.Table('cart_to_product',
                           db.Column('cart_id', db.Integer, db.ForeignKey('cart.id')),
                           db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
                           )

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    cart_id = db.relationship('Cart', backref='user', uselist=False)
    comment_id = db.relationship('Comment', backref='user', lazy='dynamic')
    # Нужен для security!
    active = db.Column(db.Boolean())
    # Для получения доступа к связанным объектам
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Flask-Security
    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    products_id = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image = db.Column(db.String(10000), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # cart_id = db.relationship('Cart', secondary=cart_to_product, backref=db.backref('product', lazy='dynamic'))
    comment_id = db.relationship('Comment', backref='product', lazy='dynamic')

    def get_id_for_carusel(self):
        id = '#' + (self.name).replace(' ', '')
        return id

    def get_href_for_carusel(self):
        return (self.name).replace(' ', '')

    def get_product_photo(self):
        if self.image:
            pattern = re.compile('\'(.*)\'')
            str_image = str(bytes(self.image))
            file_name = re.search(pattern, str_image).group(1)
            path = os.path.join(app_dir, r'app\static\img')
            if os.path.exists(os.path.join(path, file_name)):
                os.remove(os.path.join(path, file_name))
            thumb_file = (file_name.split('.'))[0] + '_thumb.jpg'
            return os.path.join('\static\img', thumb_file).replace('\\', '/')
        else:
            return '/static/img/default.png'

    def __repr__(self):
        return '<Products {}>'.format(self.name)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.relationship('Product', secondary=cart_to_product, backref=db.backref('cart', lazy='dynamic'))

    def __repr__(self):
        return '<Cart {}>'.format(self.id)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.id)
