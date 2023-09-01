from time import time
import jwt
from todo_app import app
from todo_app.models import User


def get_token(self, expires_in=180):
    return jwt.encode(
        {'user_id': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
    except:
        return None
    return User.query.get(user_id)

# from todo_app import db,login_manager,app
# from itsdangerous import URLSafeTimedSerializer
# from todo_app.models import User
#
#
# def get_token(self):
#     s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#     return s.dumps({'user_id': self.id})
#
# # @staticmethod
# def verify_token(token, expires_sec=600):
#     s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#     try:
#         user_id = s.loads(token, max_age=expires_sec)['user_id']
#     except Exception:
#         return None
#     return User.query.get(user_id)    
