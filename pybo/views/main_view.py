from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main',__name__,url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'hello, pybo!'

@bp.route('/')
def index():
    return redirect(url_for('shoes.main'))
