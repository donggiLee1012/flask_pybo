from flask import Blueprint, url_for, request, render_template,flash
import os
from werkzeug.utils import redirect,secure_filename
from werkzeug.datastructures import CombinedMultiDict
from pybo.templates.modules.initclass import *
from .. import db
from pybo.models import Shoes,Shoesmodel,Structureprice
from ..forms import SearchShoes,ShoesModelCreateForm
from pybo.views.auth_views import login_required
from sqlalchemy import func,nullslast,select
import urllib
import urllib.request
import time

from multiprocessing import Process

bp = Blueprint('model',__name__,url_prefix='/model')


@bp.route('/list/<code>')
def _list(code):
    page = request.args.get('page', type=int, default=1)
    so = request.args.get('so',type=str, default='recent')
    code=code


    #정렬
    if so == 'expensive':
        model_list = Structureprice.query.filter(Structureprice.code.ilike(code)).order_by(Structureprice.price.desc())
    elif so =='popular':
        model_list = Structureprice.query.filter(Structureprice.code.ilike(code)).order_by(Structureprice.size.desc())
    else : #최신수
        model_list = Structureprice.query.filter(Structureprice.code.ilike(code)).order_by(Structureprice.saleday.desc())


    model_list = model_list.paginate(page, per_page=10)

    return render_template('shoes/amount_model.html', model_list=model_list,page=page,so=so,code=code)

@bp.route('/create/', methods=['GET', 'POST'])
def create():
    form = ShoesModelCreateForm()
    #form = ShoesModelCreateForm(CombinedMultiDict((request.files, request.form)))
    loading = url_for('static',filename='elephant.gif')

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        brand = form.brand.data
        code = form.code.data
        color = form.colorway.data
        releasedate = form.releasedate.data
        uri=form.uri.data
        img = form.img.data

        rrrr = [name,price,brand,code,color,releasedate,img,uri]

        # 파일저장
        if img == None:
            filename = secure_filename(name)+'.jpg'
            img_path = os.path.join(
                os.getcwd(), r'pybo\static\crawling_data\model', filename)
            #urlretrieve(다운이미지경로,저장위치및이름)
            urllib.request.urlretrieve(uri, img_path)

        else:
            filename = secure_filename(img.filename)
            if name in filename :
                pass
            else:
                filename = secure_filename(name)+'.jpg'
            img.save(os.path.join(
                os.getcwd(), r'pybo\static\crawling_data\model', filename))

        model = Shoesmodel(code=code, img=filename, brand=brand,release_date=releasedate,name=name,colorway=color,retail_price=price)
        db.session.add(model)
        db.session.commit()
        howmany = process(code)

        flash(howmany)

        return redirect(url_for('model.view'))



    else:
        return render_template('shoes/shoes_model_create.html',form=form,loading=loading)




@bp.route('/view/')
def view():

    form = ShoesModelCreateForm()
    forms = form.brand.choices

    items = Shoesmodel.query.order_by(Shoesmodel.release_date.desc())
    return render_template('shoes/shoes_model_list.html',forms=forms,items=items)

def process(code):
    xxblue_total = []
    xb = Xxblue(code)
    xb.start()
    title,img_name = xb.search()
    tablenum = xb.element_generate()
    xb_obj = xb.parser()
    xb.driver.quit()


    # 모델 서브네임이없을 경우 추가한다.
    shoesmodel = Shoesmodel.query.filter(Shoesmodel.code ==code).first()
    if shoesmodel.subname == None:
        shoesmodel.subname = title

    num = 0
    # 중복값 비교
    comparison = Structureprice.query.filter(Structureprice.code.like(code)).order_by(Structureprice.id.desc()).first()

    if '없음' in xb_obj[0][0]:
        pass
    else:
        for i in xb_obj:

            size = i[0]
            price = int(i[1].replace(',', '').replace('원', ''))
            saleday = datetime.strptime(i[2], '%Y.%m.%d')
            # comparison 기존데이터 유무
            if comparison != None :
                if comparison.code == code and comparison.saleday ==saleday and comparison.price == price :
                    break
                else:
                    pass
            else : pass
            xxblue_total.insert(0, Structureprice(code=code,saleday=saleday,price=price,size=size))
            num +=1

        db.session.bulk_save_objects(xxblue_total)

    db.session.commit()

    return ('찾은값:{} DB에 저장한값:{}'.format(tablenum,num))

@bp.route('/test/')
def test22():
    #shoes = Shoesmodel.query.filter(Shoesmodel.code == 'CU6015-700').first()
    #ssssss = Structureprice.query.filter(Structureprice.code.like('CT8480-001')).order_by(Structureprice.saleday.desc()).first()

    return render_template('shoes/test2.html')