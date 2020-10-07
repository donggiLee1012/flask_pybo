from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect
from pybo.templates.modules.crawl_target import Make_driver
from .. import db
from pybo.models import Shoes
from ..forms import SearchShoes
from pybo.views.auth_views import login_required
from sqlalchemy import func,nullslast

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
    fs.driver.implicitly_wait(10)
    fs.driver.get(target+add_uri)
    if query_txt !='기본':
        fs.search()
    else: fs.driver.refresh()

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

    return redirect(url_for('shoes._list'))
    #return render_template('shoes/shoes_result.html',form=form,obj=obj)





@bp.route('/test/')
def test():

    test = Shoes.query.filter(Shoes.uri.ilike('%done=1%') | Shoes.uri.ilike('%product_status=%'))
    ts1 = Shoes.query.filter(Shoes.uri.like('%id=%'))
    cnt = test.count()
    # 삭제
    # Shoes.query.delete()
    # db.session.commit()

    return render_template('shoes/test.html',test=test,cnt=cnt,ts1=ts1)




