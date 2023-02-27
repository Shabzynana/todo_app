from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from todo_app import db, app, bcrypt
from todo_app.models import User, Todo
from todo_app.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, Change_DpForm, UpdateUserForm
from todo_app.users.token import get_token, verify_token
from todo_app.users.email import send_reset_email
from todo_app.users.picture import save_picture


users = Blueprint('users',__name__,template_folder='templates/users')


@users.route('/register', methods=['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data,username=form.username.data,first_name=form.first_name.data,last_name=form.last_name.data,gender=form.gender.data,password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Registration Completed', 'info')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)


@users.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('This is no user with this email. Please check the email or Register!', 'danger')

        elif bcrypt.check_password_hash(user.password, form.password.data) and user is not None:
            login_user(user, remember=form.remember.data)
            flash('Welcome On-board', 'info')
            return redirect(url_for('users.all_user_todos', username=current_user.username))


            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)

        elif bcrypt.check_password_hash(user.password, form.password.data) is None or user is not None:
            flash('Incorrect password', 'danger')

        else:
            flash('Login Unsuccessful. Please check email or password', 'danger')

    return render_template('login.html',form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


#send_reset_email
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):

    user = verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
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
