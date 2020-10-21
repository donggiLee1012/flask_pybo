from flask import Blueprint, url_for, request, render_template,flash
import os
from werkzeug.utils import redirect,secure_filename
from werkzeug.datastructures import CombinedMultiDict
from pybo.templates.modules.crawl_target import Make_driver
from .. import db
from pybo.models import Shoes,Shoesmodel,Structureprice
from ..forms import SearchShoes,ShoesModelCreateForm
from pybo.views.auth_views import login_required
from pybo.templates.modules.initclass import *
from sqlalchemy import func,nullslast,select
import urllib
import urllib.request
import time

from multiprocessing import Process

bp = Blueprint('shoes',__name__,url_prefix='/shoes')

@bp.route('/main/')
def main():
    #modelprice = Structureprice.query.group_by(Structureprice.code).all()
    modelprice = Structureprice.query.all()
    marketprice = Shoes.query.all()
    model = Shoesmodel.query.all()


    return render_template('shoes/shoes_main.html',modelprice=modelprice,marketprice=marketprice,model=model)


@bp.route('/search/',methods=('GET','POST'))
def search():

    form = SearchShoes()

    if request.method == 'POST' and form.validate_on_submit():

        query_txt = form.content.data
        size = form.size.data
        quantity = form.quantity.data

        howmany=process(query_txt,size,quantity)
        flash(howmany)
        return redirect(url_for('shoes._list'))
    else:
        return render_template('shoes/shoes_search.html',form=form)

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so',type=str, default='recent')


    #정렬
    if so == 'expensive':
        shoes_list = Shoes.query.order_by(Shoes.price.desc())
    elif so =='popular':
        shoes_list = Shoes.query.order_by(Shoes.size.desc())
    else : #최신수
        shoes_list = Shoes.query.order_by(Shoes.id.desc())

    #검색
    if kw:
        search = '%%{}%%'.format(kw)
        if so == 'expensive':
            shoes_list = Shoes.query.filter(Shoes.title.ilike(search) | Shoes.search_query.ilike(search)).order_by(Shoes.price.desc())
        elif so == 'popular':
            shoes_list = Shoes.query.filter(Shoes.title.ilike(search) | Shoes.search_query.ilike(search)).order_by(Shoes.size.desc())
        else:  # 최신수
            shoes_list = Shoes.query.filter(Shoes.title.ilike(search) | Shoes.search_query.ilike(search)).order_by(Shoes.id.desc())


    shoes_list = shoes_list.paginate(page, per_page=10)

    return render_template('shoes/shoes_list.html', shoes_list=shoes_list,page=page,kw=kw,so=so)


@bp.route('/detail/<int:shoes_id>/')
@login_required
def detail(shoes_id):
    shoes = Shoes.query.get_or_404(shoes_id)

    return render_template('shoes/shoes_detail.html',shoes=shoes)

def process(query_txt,size,quantity):
    total_list=[]
    # FOOTSELL CRAWLING
    fs = Foostsell(query_txt,size,quantity)
    fs.start()
    fs.search()
    fs_soup = fs.soup_make()
    fs_obj,count = fs.parser(fs_soup)
    fs.driver.quit()
    num =0
    #zip(title, condition, size, price, seller, uploadtime, uri, img)
    for title, condition, size, price, seller, uploadtime, uri, img in fs_obj:
        fs.img_save(img,img[59:])
        total_list.insert(0, Shoes(title=title, condition=condition, size=size, price=price,
                            seller=seller, upload_date=uploadtime,
                            uri=uri, search_query=query_txt, img=img))
        num +=1

    db.session.bulk_save_objects(total_list)
    db.session.commit()

    return ('찾은값:{} DB에 저장한값:{}'.format(count,num))






