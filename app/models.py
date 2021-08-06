from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


cart_to_product = db.Table('cart_to_product',
                           db.Column('cart_id', db.Integer, db.ForeignKey('cart.id')),
                           db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
                           )


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cart_id = db.relationship('Cart', backref='user', uselist=False)
    comment_id = db.relationship('Comment', backref='user', lazy='dynamic')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    image = db.Column(db.LargeBinary, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    #cart_id = db.relationship('Cart', secondary=cart_to_product, backref=db.backref('product', lazy='dynamic'))
    comment_id = db.relationship('Comment', backref='product', lazy='dynamic')

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
        return '<Comment {}'.format(self.id)
