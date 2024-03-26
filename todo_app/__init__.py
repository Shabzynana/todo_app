# import os
from flask import Flask, session
from flask_session import Session  # type: ignore

from flask_sqlalchemy import SQLAlchemy

# from flask_migrate import Migrate
# from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from todo_app.config import App_Config


db = SQLAlchemy()

bcrypt = Bcrypt()

# login_manager = LoginManager()

sess = Session()

mail = Mail()


def create_app():
    """
    Create a new instance of the app with the given configuration.

    :param config_class: configuration class
    :return: app
    """
    # Initialize Flask-

    app = Flask(__name__)
    app.config.from_object(App_Config)
#     if app.config["SQLALCHEMY_DATABASE_URI"]:
#         print(f"using db")

    # Initialize SQLAlchemy
    db.init_app(app)

    # initialise seesion
    sess.init_app(app)

    # Initialize login manager
    # login_manager.init_app(app)
    # login_manager.login_view = 'users.login' 

    # Initialize Bcrypt
    bcrypt.init_app(app)

    # Initialize Bcrypt
    mail.init_app(app)

    # Importing the models here so it can create the empty tables.
    # the routes

    from todo_app.core.views import core
    from todo_app.users.views import users
    from todo_app.todo.views import todos

    app.register_blueprint(core)
    app.register_blueprint(users)
    app.register_blueprint(todos)

    # create db tables from models if not exists
    with app.app_context():
        db.create_all()

    return app