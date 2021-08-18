from app.api import bp
from flask import jsonify
from app.models import Users,Product,Cart
from flask import request,url_for
from app import db
from app.api.errors import bad_request

@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    return jsonify(Product.query.get_or_404(id).to_dict())

@bp.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Product.to_collection_dict(Product.query, page, per_page, 'api.get_products')
    return jsonify(data)


@bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json() or {}
    if 'name' not in data or 'price' not in data or 'category_id' not in data:
        return bad_request('must include name, price and category_id fields')
    if Product.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    product = Product()
    product.from_dict(data)
    db.session.add(product)
    db.session.commit()
    response = jsonify(product.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_product', id=product.id)
    return response

@bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    pass




@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(Users.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Users.to_collection_dict(Users.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if Users.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if Users.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = Users()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    cart = user.cart_id
    if cart is None:
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass