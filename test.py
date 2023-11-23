from flask import render_template,url_for,flash,redirect,request,session
from flask_login import login_user, current_user, logout_user, login_required
from todo_app import db, bcrypt
from todo_app.models import User


def current_user_id():
    if 'user_id' in session:
        # print (session['user_id'])
        idd = session['user_id']['id']
        print (idd)
        user = User.query.filter_by(id=idd).first()
        # print (f"user: {user.username}")
        # print (f"user: {user}")
        if user:
            print (user)
            return (user)
    print('good')