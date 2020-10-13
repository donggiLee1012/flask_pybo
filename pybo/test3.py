# from models import Shoes
# from __init__ import db

import sqlite3
from templates.modules.crawl_target import Make_driver
import os
import re

if __name__ == '__main__':


    # BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pybo.db')
    BASE_DIR = os.path.join(os.path.join(os.path.pardir,'pybo.db'))

    db = sqlite3.connect(BASE_DIR)
    soup_list = []

    target = 'https://footsell.com/'
    add_uri = r'g2/bbs/board.php?bo_table=m51&r=ok'

    query_txt='기본'
    size=''
    quantity='40'

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
    cursor = db.cursor()
    result = cursor.execute(
        'select title,upload_date,img from shoes where search_query=="{query_txt}" order by id desc'.format(
            query_txt=query_txt))

    top_row = result.fetchone()
    num =0
    # print(top_row[0],top_row[1][:10],top_row[2][39:])

    for title, condition, size, price, seller, uploadtime, uri, img in objs:
        # 제목과 날짜와 업로드 이미지가 같으면 같은 게시물로 보고 중복처리
        if title == top_row[0] and uploadtime.__str__()[:10] == top_row[1][:10] and img[39:] == top_row[2][39:]:
            break
        print('{num} : {title} , {uploadtime}, {img}'.format(num=num,title=title,uploadtime=uploadtime.__str__(),img=img[39:]))
        abj_att=(title, condition, size, price, seller, uploadtime, uri, img, query_txt)
        fs.save_img(img)
        obj.insert(0,abj_att)
        num +=1

    sql = '''INSERT INTO shoes (title,condition,size,price,seller,upload_date,uri,img,search_query)
            values (?,?,?,?,?,?,?,?,?)'''

    cursor.executemany(sql,obj)

    db.commit()
    db.close()
    fs.driver.quit()
