from flask import Blueprint, url_for, request, render_template
import os
from werkzeug.utils import redirect,secure_filename
from werkzeug.datastructures import CombinedMultiDict
from pybo.templates.modules.crawl_target import Make_driver
from .. import db
from pybo.models import Shoes,Shoesmodel
from ..forms import SearchShoes,ShoesModelCreateForm
from pybo.views.auth_views import login_required
from sqlalchemy import func,nullslast,select
import urllib
import urllib.request
import time

from multiprocessing import Process

bp = Blueprint('shoes',__name__,url_prefix='/shoes')

@bp.route('/main/')
def main():
    return render_template('shoes/shoes_main.html')


@bp.route('/search/',methods=('GET','POST'))
def search():

    form = SearchShoes()

    if request.method == 'POST' and form.validate_on_submit():

        return redirect(url_for('shoes.process'),code=307)
    else:
        return render_template('shoes/shoes_search.html',form=form)






@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so',type=str, default='recent')

    # def detachedProcessFunction():
    #     i = 0
    #     while i < 4:
    #         i = i + 1
    #         print("loop running %d" % i)
    #         time.sleep(1)
    #     return url_for('shoes.main')
    #
    # global p
    # p = Process(target=detachedProcessFunction,args=())
    # p.daemon = True
    # p.start()


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
    fs.driver.implicitly_wait(10)
    fs.driver.get(target+add_uri)
    if query_txt !='기본':
        fs.footsell_search()
    else: fs.driver.refresh()

    fs.footsell_parser(soup_list)
    objs=fs.footsell_check(soup_list)

    shoes_list = Shoes.query.order_by(Shoes.id.desc()).first()

    # 데이터베이스 저장할 데이터들
    obj=[]
    for title, condition, size, price, seller, uploadtime, uri, img in objs:
        if title == shoes_list.title and uploadtime.__str__()[:10] == shoes_list.upload_date[:10] and img[39:] == shoes_list.img[39:]:
            break
        fs.footsell_save_img(img)
        obj.insert(0,Shoes(title=title, condition=condition,size=size,price=price,
              seller=seller,upload_date=uploadtime,
              uri=uri,search_query=query_txt,img=img))

    db.session.bulk_save_objects(obj)
    db.session.commit()

    fs.driver.quit()


    return redirect(url_for('shoes._list'))



    #return render_template('shoes/shoes_result.html',form=form,obj=obj)






@bp.route('/model/create/', methods=['GET', 'POST'])
def model_create():
    form = ShoesModelCreateForm()
    #form = ShoesModelCreateForm(CombinedMultiDict((request.files, request.form)))

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

        return render_template('shoes/test2.html',rrrr=rrrr)


    else:
        return render_template('shoes/shoes_model_create.html',form=form)

@bp.route('/model/view/')
def model_view():
    shosemodel = Shoesmodel.query.all()
    rrr = 'qiei'
    form = ShoesModelCreateForm()
    forms = form.brand.choices

    items = Shoesmodel.query.order_by(Shoesmodel.release_date.desc())
    return render_template('shoes/shoes_model_list.html',rrr=rrr,forms=forms,items=items)


@bp.route('/test/',methods=['GET','POST'])
def test():

    return render_template('shoes/test.html')