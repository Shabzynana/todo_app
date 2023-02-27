from todo_app import db,login_manager,app
from itsdangerous import URLSafeTimedSerializer
from todo_app.models import User


def get_token(self):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps({'user_id': self.id})

# @staticmethod
def verify_token(token, expires_sec=600):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token, max_age=expires_sec)['user_id']
    except Exception:
        return None
    return User.query.get(user_id)
