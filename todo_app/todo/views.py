import datetime
from flask import render_template,url_for,flash,request,redirect,Blueprint,abort
from flask_login import current_user,login_required
from todo_app import db
from todo_app.models import User, Todo
from todo_app.todo.forms import TodoForm

todos = Blueprint('todos',__name__,template_folder='templates/todo')


@todos.route('/create', methods=['GET','POST'])
@login_required
def create_todo():

    form = TodoForm()

    if form.validate_on_submit():

        todo = Todo(text=form.text.data,date=form.date.data,user_id=current_user.username)
        db.session.add(todo)
        db.session.commit()
        flash('Task Created!', 'info')
        return redirect(url_for('users.all_user_todos', username=current_user.username))

    return render_template('create_todo.html',form=form)

@todos.route('/todo/<int:todo_id>')
@login_required
def todo(todo_id):
    todos = Todo.query.get_or_404(todo_id)
    return render_template('todo.html',todos=todos)

@todos.route("/<int:todo_iid>/update_todo", methods=['GET', 'POST'])
@login_required
def update_todo(todo_iid):
    todo = Todo.query.get_or_404(todo_iid)
    if todo.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = TodoForm()
    if form.validate_on_submit():
        todo.text = form.text.data
        todo.date = form.date.data
        db.session.commit()
        flash('Task Updated', 'info')
        return redirect(url_for('users.all_user_todos', username=current_user.username))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.text.data = todo.text
        form.date.data = todo.date

    return render_template('create_todo.html',form=form,todo=todo)

@todos.route("/<int:todo_id>/delete", methods=['POST'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.author != current_user:
        abort(403)
    db.session.delete(todo)
    db.session.commit()
    flash('Task has been deleted', 'danger')
    return redirect(url_for('users.all_user_todos',username=current_user.username))
