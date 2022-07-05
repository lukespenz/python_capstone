from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Product, User, Cart, Image
from . import db
import json
from sqlalchemy import update
import os


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', user=current_user)


@views.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        print('posted!')
        for product in products:
            print(product.id)


@views.route('/add-cart', methods=['GET', 'POST'])
def add_cart():
    product = json.loads(request.data)
    productId = product['productId']

    item = productId
    user_id = current_user.id

    already_in_cart = db.session.query(Cart).filter(
        Cart.item == item, Cart.user_id == user_id).first()
    if already_in_cart == None:
        quantity = 1
        cart_item = Cart(item=item, quantity=quantity, user_id=user_id)
        db.session.add(cart_item)

    else:
        already_in_cart.quantity += 1

    db.session.commit()
    flash('Added to cart!', category='success')

    return jsonify({})


@views.route('/delete-cart', methods=['POST'])
def delete_cart():
    cart = json.loads(request.data)
    print('HIT ME')
    print(cart)
    cart_id = cart['productId']
    print(cart_id)

    product = Cart.query.get(cart_id)

    if product:
        db.session.delete(product)
        db.session.commit()

    return jsonify({})


@views.route('/delete-product', methods=['POST'])
def delete_product():
    product = json.loads(request.data)
    productId = product['productId']
    product = Product.query.get(productId)
    image = Image.query.get(productId)
    print(image.image)
    img_file_path = 'website/static/img/products/' + image.image

    if os.path.exists(img_file_path):
        os.remove(img_file_path)

    if product:
        db.session.delete(product)
        db.session.delete(image)
        db.session.commit()

    return jsonify({})


@views.route('/checkout', methods=['POST'])
def checkout():
    user = json.loads(request.data)
    user_id = user['userId']

    cart = Cart.query.filter_by(user_id=user_id).all()

    for item in cart:
        remove_cart = Cart.query.get(item.id)
        db.session.delete(remove_cart)
        db.session.commit()

    flash('Checked out, your order is on its way!', category='success')

    return jsonify({})
