from flask import Blueprint, url_for, request, render_template,g,flash
import js2py



bp = Blueprint('stockx',__name__,url_prefix='/stockx')
js2py

@bp.route('/main')
def main():
    js2py.translate_file('index.js', 'index.py')

    #form = js2py.require(url_for('static',filename='nodejs/app.js'))
    #StockXAPI = js2py.require('stockx-api')
    return render_template('stockx/stockx.html')
