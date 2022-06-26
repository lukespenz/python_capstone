from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    category = db.Column(db.String(150))
    type = db.Column(db.String(150))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    on_display = db.Column(db.Boolean)
    description = db.Column(db.String(2000))


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    image = db.Column(db.String(1000))
    created = db.Column(db.DateTime(timezone=True), default=func.now())


# class Users_Cart(db.Model):
#     user = db.Column(db.Integer, db.ForeignKey('user.id'))
#     product = db.Column(db.Integer, db.ForeignKey('product.id'))
#     quantity = db.Column(db.Integer)
