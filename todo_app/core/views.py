from flask import render_template,request,Blueprint


core = Blueprint('core',__name__,template_folder='templates/core')

@core.route('/')
def index():
    return render_template('main.html')
