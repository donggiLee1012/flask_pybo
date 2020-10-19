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

    query_txt = '오프화이트 러버덩크'
    size = ''
    quantity = '100'

    bg = Make_driver('bgjt',query_txt,quantity)
    bg.bgjt_search()
    bg.bgjt_parser(soup_list)
    print(soup_list)
    objs = bg.bgjt_check(soup_list)

    num = 0
    obj = []
    cursor = db.cursor()
    for title, condition, size, price, seller, uploadtime, uri, img in objs:
        print('{num} : {title} , {price},{uploadtime}\n\n'.format(num=num, title=title, uploadtime=uploadtime.__str__(),
    price=price))
        abj_att = (title, condition, size, price, seller, uploadtime, uri, img, query_txt)

        obj.insert(0, abj_att)
        num += 1

    sql = '''INSERT INTO shoes (title,condition,size,price,seller,upload_date,uri,img,search_query)
                values (?,?,?,?,?,?,?,?,?)'''
    cursor.executemany(sql, obj)

    db.commit()
    db.close()

    bg.driver.quit()


