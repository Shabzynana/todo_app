import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_moment import Moment


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysegcret'

########################   ####################

        # SQL DATABASE AND MODELS

##########################################
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://shabzy:RcvUfShcM9KhH3dLDH3cnCvS5E9dtGNC@dpg-cfuit7en6mps93386tm0-a.oregon-postgres.render.com/todo_app_dvp4'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

bcrypt = Bcrypt(app)

moment = Moment(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['TESTING'] = False
app.config['MAIL_USERNAME'] = 'shabzynana@gmail.com'
app.config['MAIL_PASSWORD'] = ''


mail = Mail(app)


from todo_app.core.views import core
from todo_app.users.views import users
from todo_app.todo.views import todos


# from shabzyblog.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(todos)


# app.register_blueprint(error_pages)
