from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.models import Users, Category, Product, Comment, Cart
from app.forms import RegistrationForm, LoginForm, CommentForm


@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        count = len(cart.product_id)
        return render_template('index.html', form1=form, count=count)
    return render_template('index.html', form1=form)


@app.route('/register', methods=['GET', 'POST'])
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
    return render_template('register.html', title='Регистрация', form2=form2, form1=form1)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form1 = LoginForm()
    if form1.validate_on_submit():
        user = Users.query.filter_by(username=form1.username.data).first()
        if user is None or not user.check_password(form1.password.data):
            flash('Неправильный ник или пароль')
            return render_template('index.html', form1=form1)
        login_user(user, remember=form1.remember_me.data)
        cart = user.cart_id
        if cart is None:
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form1=form1, count=None)


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли с аккаунта')
    return redirect(url_for('index'))


@login_required
@app.route('/catalog', methods=['GET'])
def catalog():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    count = len(cart.product_id)
    categories = Category.query.all()
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('catalog', page=products.next_num) if products.has_next else None
    prev_url = url_for('catalog', page=products.prev_num) if products.has_prev else None
    return render_template('catalog.html', categories=categories, products=products.items, title='Каталог',
                           next_url=next_url, prev_url=prev_url, count=count)


@login_required
@app.route('/catalog/<int:category_id>', methods=['GET'])
def category(category_id):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    count = len(cart.product_id)
    categories = Category.query.all()
    products_by_category = Product.query.filter_by(category_id=category_id)
    page = request.args.get('page', 1, type=int)
    products = products_by_category.paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('category', page=products.next_num, category_id=category_id) if products.has_next else None
    prev_url = url_for('category', page=products.prev_num, category_id=category_id) if products.has_prev else None
    return render_template('catalog.html', categories=categories, products=products.items, title='Каталог',
                           next_url=next_url, prev_url=prev_url, count=count)


@login_required
@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    count = len(cart.product_id)
    form = CommentForm()
    product = Product.query.get(product_id)
    comments = Comment.query.filter_by(product_id=product.id).all()
    if form.validate_on_submit():
        c = Comment(text=form.text.data, user_id=current_user.id, product_id=product.id)
        db.session.add(c)
        db.session.commit()
        flash('Отзыв успешно добавлен')
        return redirect(url_for('product', product_id=product.id))
    return render_template('product.html', product=product, form=form, comments=comments, count=count)


@login_required
@app.route('/add/<int:product_id>', methods=['GET', 'POST'])
def update_cart(product_id):
    form = CommentForm()
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    product = Product.query.get(product_id)
    comments = Comment.query.filter_by(product_id=product.id).all()
    if product in cart.product_id:
        flash('Товар уже в корзине!')
    else:
        cart.product_id.append(product)
        cart.total_price += product.price
        db.session.add(cart)
        db.session.commit()
        flash('Продукт добавлен в корзину')
    count = len(cart.product_id)
    return render_template('product.html', product=product, form=form, comments=comments, count=count)


@login_required
@app.route('/cart/<int:cart_id>')
def cart(cart_id: int):
    cart = Cart.query.get(cart_id)
    count = len(cart.product_id)
    products = cart.product_id
    return render_template('cart.html', products=products, count=count, cart=cart)


@login_required
@app.route('/remove/<int:product_id>/<int:cart_id>')
def remove(product_id: int, cart_id):
    cart = Cart.query.get(cart_id)

