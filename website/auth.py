from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Product
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exit.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/add_products', methods=['GET', 'POST'])
@login_required
def add_products():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        type = request.form.get('type')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        description = request.form.get('description')

        if request.form.get('on_display') == 'on':
            on_display = True
        else:
            on_display = False

        new_product = Product(name=name, category=category, type=type, price=price,
                              quantity=quantity, on_display=on_display, description=description)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added!', category='success')

        return render_template('products.html', user=current_user)

    return render_template('add_products.html', user=current_user)


@auth.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    products = Product.query.all()
    print(products)
    return render_template('products.html', user=current_user, products=products)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be more than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
