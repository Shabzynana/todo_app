import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_moment import Moment


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

########################   ####################

        # SQL DATABASE AND MODELS

##########################################
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

bcrypt = Bcrypt(app)

# moment = Moment(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['TESTING'] = False
app.config['MAIL_USERNAME'] = os.environ.get("USER_DB")
app.config['MAIL_PASSWORD'] = os.environ.get("PASSWORD_DB")


mail = Mail(app)


from todo_app.core.views import core
from todo_app.users.views import users
from todo_app.todo.views import todos



app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(todos)
