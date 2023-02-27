from flask import url_for, render_template
from flask_mail import Message

from todo_app import mail
from todo_app.users.token import get_token, verify_token

def send_reset_email(user):
    token = get_token(user)
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.html = render_template('activate.html', token=token, _external=True)
    mail.send(msg)
