from flask import render_template,url_for,flash,redirect,request,Blueprint,session
# from flask_login import login_user, current_user, logout_user, login_required
from todo_app import db, bcrypt
from todo_app.models import User, Todo
from todo_app.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, Change_DpForm, UpdateUserForm
from todo_app.users.token import verify_token
from todo_app.users.email import send_reset_password, send_email, resend_email
from todo_app.users.picture import save_picture, current_user_id, login_required

import datetime

users = Blueprint('users',__name__,template_folder='templates/users')



@users.route('/me')
def home():

    sam = current_user_id().email
    print(sam)
    return (f'Hello, {sam.username} (ID: {sam.id})!')
    # return ("settos")


@users.route('/register', methods=['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data,username=form.username.data,first_name=form.first_name.data,last_name=form.last_name.data,gender=form.gender.data,password=hashed_password,confirmed=False)

        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('Registration Completed', 'info')
        # flash('An email has been sent with instructions to verify your account.', 'info')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)




@users.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        # session['username'] = request.form['username']

        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            print("no user")
            flash('This is no user with this email. Please check the email or Register!', 'danger')


        elif bcrypt.check_password_hash(user.password, form.password.data) and user is not None:
            # session['user_id'] = user['id']  # Store user's ID in the session

            session['logged_in'] = True
            session["user_id"] = {"id": user.id}
            session["username"] = {"username" : user.username}
            session["confirmed"] = {"confirmed" : user.confirmed}

            # session["username"] = {"username": user.username}


            # session.permanent = True  # Use cookie to store session.
            print(f'login in gee {user.id}')
            # print(f'login in gee {session.username}')

            flash('You are now logged in.', 'success')
         
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)

        elif bcrypt.check_password_hash(user.password, form.password.data) is None or user is not None:
        # elif bcrypt.check_password_hash(user.password, form.password.data) is None:
            flash('Incorrect password', 'danger')

        else:
            flash('Login Unsuccessful. Please check email or password', 'danger')

    return render_template('login.html',form=form)





@users.route("/logout")
def logout():
  
    # session.pop('logged_in', None)
    # session.pop('username', None)
    # flash('M out', 'danger')

    session.clear()
    flash('M out', 'info')

    return redirect(url_for("core.index"))




@users.route('/email_confirmation/resend')
def resend():

    resend_email(current_user)
    flash('A new confirmation mail has been sent with instructions to verify your account.', 'info')
    return redirect(url_for('users.unconfirmed'))



@users.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user_id().confirmed:
        return redirect('core.index')
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')



@users.route('/confirm/<token>')
def confirm_email(token):

    tok = verify_token(token)
    if tok is None:
        flash('That is an invalid or expired link', 'danger')
        return redirect(url_for('core.index'))
    user = User.query.filter_by(id=tok.id).first_or_404()
    if user.confirmed:
        flash(f"Account already confirmed : {user.username}", 'success')
        return redirect(url_for('core.index'))
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash(f"You have confirmed your account. Thanks {user.username}", 'success')
    return redirect(url_for('core.index'))



#send_reset_email
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_password(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)



@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):

    user = verify_token(token)
    if user is None:
        flash('That is an invalid or expired link', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password Updated! log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/<username>", methods=['GET','POST'])
def user_todos(username):

    user = User.query.filter_by(username=username).first_or_404()

    form = Change_DpForm()
    if form.validate_on_submit():

        if form.picture.data:
            pic = save_picture(form.picture.data)
            current_user.profile_image = pic
        db.session.commit()
        flash('Profile Image Updated!', 'info')
        return redirect(url_for('users.user_todos', username=current_user.username))

    ROWS_PER_PAGE = 4
    page = request.args.get('page',1,type=int)
    todos = Todo.query.filter_by(author=user).order_by(Todo.date.desc()).paginate(page=page,per_page=ROWS_PER_PAGE)
    return render_template('user_todos.html',todos=todos,user=user,page=page,form=form)


@users.route("/todo/<username>", methods=['GET','POST'])
@login_required
# @user_check
def all_user_todos(username):

    user = User.query.filter_by(username=username).first_or_404()
    ROWS_PER_PAGE = 5
    page = request.args.get('page',1,type=int)
    todos = Todo.query.filter_by(author=user).order_by(Todo.date.asc()).paginate(page=page,per_page=ROWS_PER_PAGE)

    return render_template('all_user_todo.html',todos=todos,user=user,page=page)

@users.route('/account', methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('User Account Updated!', 'info')
        return redirect(url_for('users.user_todos', username=current_user.username))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username

    return render_template('account.html',form=form)
