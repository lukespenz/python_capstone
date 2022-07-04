from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Product, User, Cart, Image
from . import db
import json
from sqlalchemy import update
import os


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template('home.html', user=current_user)


@views.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        print('posted!')
        for product in products:
            print(product.id)


@views.route('/add-cart', methods=['GET', 'POST'])
@login_required
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


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/delete-product', methods=['POST'])
def delete_product():
    product = json.loads(request.data)
    productId = product['productId']
    product = Product.query.get(productId)
    image = Image.query.get(productId)
    print(image.image)
    img_file_path = 'website/static/img/' + image.image

    if os.path.exists(img_file_path):
        os.remove(img_file_path)

    if product:
        db.session.delete(product)
        db.session.delete(image)
        db.session.commit()

    return jsonify({})
