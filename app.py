from flask import render_template
from todo_app import create_app
# from todo_app.users.picture import current_user_id

app = create_app()

# @app.route('/d')
# def index():
#     return render_template('base.html', current_user=current_user_id())

if __name__ == "__main__":
    app.run(debug=True)

