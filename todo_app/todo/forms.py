from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField

from wtforms.validators import DataRequired


class TodoForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    text = TextAreaField('Task:', validators=[DataRequired(message = "Fill in Task")])
    date = DateField('Date:')
    submit = SubmitField('Post')

# , format='%m/%d/%y'
# {{url_for('todos.update',todo_iid=todos.id)}}
