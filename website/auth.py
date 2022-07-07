from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Product, MyForm, Cart, Image
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import json
import os

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
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/product_showcase/<int:id>', methods=['POST', 'GET'])
@login_required
def product_showcase(id):
    product_id = id
    print(product_id)
    product = Product.query.get(product_id)
    image = Image.query.get(product_id)

    return render_template("product_showcase.html", user=current_user, product=product, image=image)


@auth.route('/add_products', methods=['GET', 'POST'])
@login_required
def add_products():
    user = current_user
    print(user.admin)
    if user.admin == True:
        form = MyForm()

        if form.validate_on_submit():
            img_name = request.form.get('img_name')
            filename = secure_filename(form.image.data.filename)
            sliced = slice(filename.find('.'), len(filename))
            file_type = filename[sliced]
            image = img_name + file_type

            # checks database to see if image name taken
            image_name_taken = Image.query.filter_by(image=image).first()

            if image_name_taken != None:
                flash(
                    'Image name already taken. Please choose unique name.', category='error')
                return render_template('add_products.html', user=current_user, form=form)

            # saves image in static/img folder
            form.image.data.save('website/static/img/products/' + image)

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

                product = Product.query.filter_by(name=name).first()
                product_id = product.id
                new_image = Image(product_id=product_id, image=image)
                db.session.add(new_image)
                db.session.commit()
                flash('Product added!', category='success')
                return products()

        return render_template('add_products.html', user=current_user, form=form)
    else:
        return render_template('error.html')


@auth.route('/products', methods=['GET', 'POST'])
def products():
    products = Product.query.all()[::-1]
    images = Image.query.all()[::-1]
    return render_template('products.html', user=current_user, products=products, images=images)


@auth.route('/error')
def error():
    return render_template('error.html', user=current_user)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
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
            new_user = User(email=email, first_name=first_name, last_name=last_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)


@auth.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    cart = Cart.query.all()
    images = Image.query.all()
    cart_list = []
    images_list = []
    subtotal = 0
    user = current_user
    user_id = user.id

    for item in cart:
        if current_user.id == item.user_id:
            product_id = item.item
            product = Product.query.filter_by(id=product_id).first()
            name = product.name
            print(product)
            print(name)
            id = item.id
            quantity = item.quantity
            price = product.price
            subtotal += price
            category = product.category

            item = [name, quantity, id, price, category]
            cart_list.append(item)

            for image in images:
                if image.product_id == product_id:
                    img = image.image
                    images_list.append(img)

    paired_list = list(zip(cart_list, images_list))
    print(cart_list, images_list)
    print(subtotal)

    return render_template('shopping_cart.html', user=current_user, cart=cart, images=images, carted=paired_list, subtotal=subtotal, user_id=user_id)


@auth.route('/about_us')
def about_us():
    return render_template('about_us.html', user=current_user)


@auth.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Contact form successfully submitted', category="success")

    return render_template('contact.html', user=current_user)


@auth.route('/FAQs')
def faqs():
    return render_template('FAQs.html', user=current_user)


@auth.route('/update_product/<int:id>', methods=['GET', 'POST'])
@login_required
def update_product(id):
    product_id = id
    product = Product.query.get(product_id)
    img_name = request.form.get('img_name')

    form = MyForm()

    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        sliced = slice(filename.find('.'), len(filename))
        file_type = filename[sliced]
        image = img_name + file_type
        img_file_path = 'website/static/img/products/'
        print('here')
        print(len(image))

        # checks database to see if image name taken
        image_name_taken = Image.query.filter_by(image=image).first()

        if image_name_taken != None:
            flash('Image name already taken. Please choose unique name.',
                  category='error')
            return render_template('update_product.html', user=current_user, form=form, product=product)

        # saves image in static/img folder
        if image != '':
            update_image = Image.query.get(product_id)

            if os.path.exists(img_file_path + image):
                os.remove(img_file_path + image)

            if os.path.exists(img_file_path + update_image.image):
                os.remove(img_file_path + update_image.image)

            form.image.data.save('website/static/img/products/' + image)
            update_image = Image.query.get(product_id)
            update_image.image = image

        if request.method == 'POST':
            product.name = request.form['name']
            product.category = request.form['category']
            product.type = request.form['type']
            product.price = request.form['price']
            product.quantity = request.form['quantity']
            product.description = request.form['description']

            if request.form.get('on_display') == 'on':
                product.on_display = True
            else:
                product.on_display = False

            try:
                # db.session.add(product)
                db.session.commit()

                flash(
                    f'Product { product.name } successfully updated!', category='success')
                return redirect('/products')
            except:
                return flash('Error: problem updating product')

        # else:
        #     return render_template('update_product.html', product=product)

    return render_template('update_product.html', user=current_user, form=form, product=product)
