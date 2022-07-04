from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, environ
from flask_login import LoginManager
# from flask_uploads import configure_uploads, IMAGES, UploadSet
secret_key = 'ThisIsTheOnlyWay123456789!'
DB_NAME = 'postgresql://lqgcillqgzgbeq:aceb31140dd8d60e636739409de9777fab93d8f6dad355d4ea3b0bf029b0ee81@ec2-3-224-8-189.compute-1.amazonaws.com:5432/dd81aird9bek3k'
db = SQLAlchemy()
# secret_key = environ['secret_key']
# DB_NAME = environ['DB_NAME']


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOADED_IMAGES_DEST'] = 'static/img'
    db.init_app(app)

    # images = UploadSet('images', IMAGES)
    # configure_uploads(app, images)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Product, Image, Cart

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
