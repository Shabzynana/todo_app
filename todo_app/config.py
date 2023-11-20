"""
summary
"""
import os
import datetime
from dotenv import load_dotenv


load_dotenv(".env")


# pylint: disable=invalid-name
class App_Config:
    """_summary_"""

    SECRET_KEY = os.getenv("SECRET_KEY", "test")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


    # SESSION CONFIG
    SESSION_TYPE = "filesystem" if not os.getenv("PROD", None) else "sqlalchemy"
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_HTTPONLY = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

    ## MAIL CONFIG
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("USER_MAIL")
    MAIL_PASSWORD = os.getenv("PASSWORD_MAIL")












# app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# # app.config['MAIL_PORT'] = 465
# # app.config['MAIL_USE_SSL'] = True
# # app.config['TESTING'] = False
# app.config['MAIL_USERNAME'] = os.getenv("USER_MAIL")
# app.config['MAIL_PASSWORD'] = os.getenv("PASSWORD_MAIL")

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
# # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

