from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time,re
import math
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
    # --------OK------------

    objs=fs.check(soup_list)


    # db.session.commit()
    #
    obj=[]
    for title, condition, size, price, seller, uploadtime, uri, img in objs:
        obj.append(Shoes(title=title, condition=condition,size=size,price=price,
              seller=seller,upload_date=uploadtime,
              uri=uri,search_query=query_txt))

    db.session.bulk_save_objects(obj)
    db.session.commit()

    fs.driver.quit()
    del fs
    # shoes = Shoes(title=title, create_date=datetime.date(datetime.now()), )
    # db.session.add(shoes)
    # db.session.commit()
    return render_template('shoes/shoes_result.html',form=form,obj=obj)





