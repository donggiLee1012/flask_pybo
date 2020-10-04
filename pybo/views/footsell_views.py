from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time,re
import math

import urllib
import urllib.request
import requests

from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect
from pybo.templates.modules.crawl_target import Make_driver
from .. import db
from pybo.models import Shoes
from datetime import datetime
from ..forms import SearchShoes


bp = Blueprint('shoes',__name__,url_prefix='/shoes')

@bp.route('/main/',methods=('GET','POST'))
def main():

    form = SearchShoes()

    if request.method == 'POST' and form.validate_on_submit():

        return redirect(url_for('shoes.process'),code=307)
    else:
        return render_template('shoes/main.html',form=form)


@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    shoes_list = Shoes.query.order_by(Shoes.upload_date.desc())
    shoes_list = shoes_list.paginate(page, per_page=10)
    return render_template('shoes/shoes_list.html', shoes_list=shoes_list)

@bp.route('/detail/<int:shoes_id>/')
def detail(shoes_id):
    shoes = Shoes.query.get_or_404(shoes_id)

    return render_template('shoes_detail.html',shoes=shoes)


@bp.route('/footsell',methods=('GET','POST'))
def process():
    soup_list=[]
    form = SearchShoes()
    target = 'https://footsell.com/'
    add_uri = r'g2/bbs/board.php?bo_table=m51&r=ok'

    size = form.size.data
    query_txt = form.content.data
    quantity = form.quantity.data

    fs = Make_driver(query_txt,size,quantity)
    fs.driver.get(target+add_uri)
    fs.driver.implicitly_wait(10)
    fs.search()
    fs.parser(soup_list)
    objs=fs.check(soup_list)

    # 데이터베이스 저장할 데이터들
    obj=[]
    for title, condition, size, price, seller, uploadtime, uri, img in objs:
        obj.append(Shoes(title=title, condition=condition,size=size,price=price,
              seller=seller,upload_date=uploadtime,
              uri=uri,search_query=query_txt,img=img))

    db.session.bulk_save_objects(obj)
    db.session.commit()

    fs.driver.quit()
    del fs
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')


    return render_template('shoes/shoes_result.html',form=form,obj=obj)

@bp.route('/')
def test():
    soup_list = []
    form = SearchShoes()
    target = 'https://footsell.com/'
    add_uri = r'g2/bbs/board.php?bo_table=m51&r=ok'


    fs = Make_driver()
    fs.driver.get(target + add_uri)
    fs.driver.implicitly_wait(10)
    fs.parser(soup_list)
    objs = fs.check(soup_list)
    obj=[]


    for title, condition, size, price, seller, uploadtime, uri, img in objs:
        obj.append(Shoes(title=title, condition=condition,size=size,price=price,
              seller=seller,upload_date=uploadtime,
              uri=uri,search_query='',img=img))

        fs.save_img(img,uri)



    db.session.bulk_save_objects(obj)
    db.session.commit()

    fs.driver.quit()


    return render_template('shoes/test.html',soup_list=soup_list)

@bp.route('/test2/<uri>')
def test2(uri):
    img_uri = uri
    urllib.request.urlretrieve('https://footsell.com'+img_uri,'test.jpg')

    return render_template('shoes/test2.html')




