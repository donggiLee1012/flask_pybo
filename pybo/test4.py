import sqlite3
from templates.modules.crawl_target import Make_driver
import os
import time

if __name__ =='__main__':
    BASE_DIR = os.path.join(os.path.join(os.path.pardir,'pybo.db'))

    db = sqlite3.connect(BASE_DIR)

    query_txt = '오프화이트'

    xb = Make_driver('xxblue')

    title,uri,img_name = xb.xxblue_search(query_txt)

    xb.xxblue_element_generate()

    objs,shoesmodel_id = xb.xxblue_parser()

    xb.driver.quit()

    print(objs)


    # 데이터베이스 저장할 데이터들

    obj = []
    cursor = db.cursor()

    condition = '검수상품'
    seller = 'xxblue'
    img = img_name
    uri = uri
    shoesmodel_id = shoesmodel_id
    for i in objs:
        size = i[0]
        price = i[1].replace(',','').replace('원','')
        uploadtime = i[2]
        abj_att = (title, condition, size, price, seller, uploadtime, uri, img, query_txt,shoesmodel_id)
        obj.insert(0, abj_att)

    sql = '''INSERT INTO shoes (title,condition,size,price,seller,upload_date,uri,img,search_query,shoesmodel_id)
                values (?,?,?,?,?,?,?,?,?,?)'''

    cursor.executemany(sql, obj)

    db.commit()
    db.close()
    xb.driver.quit()





