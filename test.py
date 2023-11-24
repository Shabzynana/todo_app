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



            <div class="navbar-nav">

              {% if session.logged_in and session.confirmed %}

              <li><a href="#ss">Drafts</a></li>
              <li><a href="#">Create Entry</a></li>
              <a class="nav-item nav-link" href="{{ url_for('users.logout') }}">Logout</a>

              {% elif session.logged_in %}
              <li><a href="#">Unconfirmed</a></li>
              <a class="nav-item nav-link" href="{{ url_for('users.logout') }}">Logout</a>

              {% else %}

              <a class="nav-item nav-link" href="{{ url_for('users.login') }}">Login</a>
              <a class="nav-item nav-link" href="{{ url_for('users.register') }}">Register</a>

              {% endif %}
            </div

