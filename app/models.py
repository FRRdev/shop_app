import re
from flask import url_for
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_security import RoleMixin
import os
from config import app_dir
from datetime import datetime,timedelta
import base64
import os

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


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


class Users(PaginatedAPIMixin, UserMixin, db.Model):
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
    token_expiration = db.Column(db.DateTime) #время жизни токена
    token = db.Column(db.String(32), index=True, unique=True)
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

    def to_dict(self, include_email=False):
        products = ",".join([str(product.name) for product in self.cart_id.product_id]) if len(
            self.cart_id.product_id) != 0 else None
        data = {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'count_products': len(self.cart_id.product_id),
            'cart': {
                'cart_id': self.cart_id.id,
                'products': products,
            },
            '_links': {
                'self': url_for('api.get_user', id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'first_name', 'last_name']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = Users.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    products_id = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Product(PaginatedAPIMixin, db.Model):
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

    def to_dict(self):
        cart_id = ",".join([str(cart.id) for cart in self.cart.all()]) if len(self.cart.all()) != 0 else None
        data = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'count_cart': self.cart.count(),
            'id_cart': cart_id,
            '_links': {
                'self': url_for('api.get_product', id=self.id),
                'image': self.get_product_photo()
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'price', 'description','category_id']:
            if field in data:
                setattr(self, field, data[field])


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_price = db.Column(db.Float, default=0)
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
