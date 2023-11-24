import os
import secrets
from PIL import Image
from flask import url_for, flash, current_app, redirect, session
# from flask_login import current_user
from functools import wraps

from todo_app.models import User

def current_user_id():
    if 'user_id' in session:
        idd = session['user_id']['id']
        user = User.query.filter_by(id=idd).first()
        if user:
            return user
    return None       


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user_id().confirmed is False:
            return redirect(url_for('users.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function



# def user_check(func):
#     @wraps(func)
#     def decorated_function(username, *args, **kwargs):
#         user = User.query.filter_by(username=username).first()
#         if current_user != user:
#             flash('User not authorized', 'danger')
#             return redirect(url_for('users.all_user_todos', username=current_user.username))
#         return func(username, *args, **kwargs)

#     return decorated_function


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return func(*args, **kwargs)
        return redirect(url_for('users.login'))
    return inner

