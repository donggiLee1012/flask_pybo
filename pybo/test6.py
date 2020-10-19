# from models import Shoes
# from __init__ import db

import sqlite3
from templates.modules.initclass import *
import os
import re

if __name__ == '__main__':

    # BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pybo.db')
    BASE_DIR = os.path.join(os.path.join(os.path.pardir,'pybo.db'))

    db = sqlite3.connect(BASE_DIR)
    cursor = db.cursor()

    query_txt = '오프화이트 러버덩크'
    size = ''
    quantity = '100'

    total_list=[]

    fs = Foostsell(query_txt)
    fs.start()
    fs.search()
    fs_soup = fs.soup_make()
    fs_obj = fs.parser(fs_soup)
    fs.driver.quit()
    #zip(title, condition, size, price, seller, uploadtime, uri, img)
    for title, condition, size, price, seller, uploadtime, uri, img in fs_obj:
        fs.img_save(img,img[59:])
        abj_att = (title, condition, size, price, seller, uploadtime, uri, img, query_txt)
        total_list.insert(0, abj_att)


    xb = Xxblue(query_txt)
    xb.start()
    xb_title,xb_uri,xb_img_name = xb.search()
    xb.element_generate()
    xb_obj,xb_shoes_modelid = xb.parser()
    xb.driver.quit()
    xb_condition = '검수상품'
    xb_seller = 'xxblue'
    # xb_title
    for i in xb_obj:
        size = i[0]
        price = i[1].replace(',','').replace('원','')
        uploadtime = i[2]
        abj_att = (xb_title, xb_condition, size, price, xb_seller, uploadtime, xb_uri, xb_img_name, query_txt)
        total_list.insert(0, abj_att)


    bg = Bgjt(query_txt)
    bg.start()
    bg.search()
    bg_soup = bg.soup_make()
    bg_obj = bg.parser(bg_soup)
    bg.driver.quit()
    #zip(title, condition, size, price, seller, uploadtime, uri, img)
    for title, condition, size, price, seller, uploadtime, uri, img in bg_obj:
        abj_att = (title, condition, size, price, seller, uploadtime, uri, img, query_txt)
        bg.img_save(img, img[36:])
        total_list.insert(0, abj_att)


#(title, condition, size, price, seller, uploadtime, uri, img, query_txt, shoesmodel_id)


    sql = '''INSERT INTO shoes (title,condition,size,price,seller,upload_date,uri,img,search_query)
                values (?,?,?,?,?,?,?,?,?)'''
    cursor.executemany(sql, total_list)
    db.commit()
    db.close()
    bg.driver.quit()


