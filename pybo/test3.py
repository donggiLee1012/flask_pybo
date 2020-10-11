# from models import Shoes
# from __init__ import db

import sqlite3
from templates.modules.crawl_target import Make_driver
import os

if __name__ == '__main__':
    # BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pybo.db')
    BASE_DIR = os.path.join(os.path.join(os.path.pardir,'pybo.db'))

    db = sqlite3.connect(BASE_DIR)

    soup_list = []

    target = 'https://footsell.com/'
    add_uri = r'g2/bbs/board.php?bo_table=m51&r=ok'

    query_txt='기본'
    size=''
    quantity='30'

    fs = Make_driver(query_txt, size, quantity)
    fs.driver.implicitly_wait(10)
    fs.driver.get(target + add_uri)
    if query_txt != '기본':
        fs.search()
    else:
        fs.driver.refresh()

    fs.parser(soup_list)
    objs = fs.check(soup_list)

    # 데이터베이스 저장할 데이터들
    obj = []

    for title, condition, size, price, seller, uploadtime, uri, img in objs:
        abj_att=(title, condition, size, price, seller, uploadtime, uri, img, '테스트')
        obj.append(abj_att)

    sql = '''INSERT INTO shoes (title,condition,size,price,seller,upload_date,uri,img,search_query)
            values (?,?,?,?,?,?,?,?,?)'''

    cus =db.cursor()
    cus.executemany(sql,obj)

    db.commit()
    db.close()
    fs.driver.quit()


    # for title, condition, size, price, seller, uploadtime, uri, img in objs:
    #     obj.append(Shoes(title=title, condition=condition, size=size, price=price,
    #                      seller=seller, upload_date=uploadtime,
    #                      uri=uri, search_query=query_txt, img=img))
    #
    # db.session.bulk_save_objects(obj)
    # db.session.commit()
    #
    # fs.driver.quit()
