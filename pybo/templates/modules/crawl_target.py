from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os,re,time,sys
from datetime import datetime
import math

import urllib
import urllib.request
import requests

# sys.path.append('/c/projects/firstproject/pybo')

from pybo import db
from pybo.models import Shoes



class Make_driver:
    robots = 'robots.txt'
    driverpath = r'C:\projects\firstproject\pybo\static\chromedriver.exe'

    def __init__(self,query_txt='',size='',quantity=90):
        self.driver = webdriver.Chrome(Make_driver.driverpath)
        self.query_txt = query_txt
        if size =='':
            self.size=''
        else:
            self.size = int(size)
        self.quantity = quantity
        self.time_marker = time.strftime('%Y-%m-%d_%H%M', time.localtime())

        self.img_path = r'C:\projects\firstproject\pybo\static\crawling_data\{}'.format(self.time_marker)

        if os.path.exists(self.img_path):
            pass
        else:
            os.makedirs(self.img_path)


    def parser(self,soup_list=[]):

        for j in range(math.ceil(int(self.quantity) / 40)):
            time.sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            time.sleep(1)
            border_list = soup.find_all(id=re.compile('list_row_'))


            if border_list == []:
                border_list='결과안잡힘'
                soup_list.append(border_list)
                break

            if self.query_txt =='':
                border_list = border_list[3:]

            soup_list.append(border_list)

            try:
                self.driver.find_elements(By.CSS_SELECTOR, 'ul>li>a')[j].send_keys(Keys.ENTER)
            except:
                break



    def search(self):
        # 검색
        search_box = self.driver.find_element_by_css_selector('#list_search_text_input')
        search_box.send_keys(self.query_txt)
        search_box.send_keys(Keys.ENTER)

        # 사이즈별 선택한게있으면 실행
        if self.size != '':
            input_size = 'option[value="' + '{}"]'.format(self.size)
            size_select = self.driver.find_element(By.CSS_SELECTOR, input_size)
            size_select.click()


    def check(self, soup_list):
        title=[]
        condition=[]
        size = []
        price = []
        seller = []
        uploadtime = []
        uri = []
        img = []

        count=0

        for border_list in soup_list:

            for border_list_att in border_list:
                # 제목
                try:
                    title_att = border_list_att.find('span', id=re.compile('^list_subject_')).text.strip()

                except:
                    title_att = border_list_att.find('span', class_='smallfont color_aaa').text.strip()

                # 컨디션
                condition_att = border_list_att.find('span', class_='list_market_used han').text

                # 사이즈
                size_att = border_list_att.find('span', class_='list_market_size').text

                # 가격
                try:
                    price_att = border_list_att.find('div', class_=re.compile('^list_market_price')).text.strip()
                except:
                    price_att = border_list_att.find('span', class_='color_aaa normal smallfont').text.strip()

                # 판매자명
                seller_att = border_list_att.find('div', class_=re.compile('^float_left list_market_name')).text.strip()

                # 업로드 시각
                uploadtime_att = border_list_att.find('span', class_='list_table_dates').text.strip()

                # uri
                uri_att = border_list_att.find('a').get('href')

                # img
                img_att = border_list_att.find('img').get('src')

                if ':' in uploadtime_att:
                    uploadtime_att = datetime.date(datetime.now())
                else:

                    uploadtime_att = datetime.strptime('20'+uploadtime_att,'%Y-%m-%d').date()

                title.append(title_att)
                condition.append(condition_att)
                size.append(size_att)
                price.append(price_att)
                seller.append(seller_att)
                uploadtime.append(uploadtime_att)
                uri.append(uri_att)
                img.append(img_att)

                count += 1
                if count == self.quantity:
                    break

        return zip(title, condition, size, price, seller, uploadtime, uri, img)

    def save_img(self,img_url,num,query_txt=''):

        # b_id = re.search('(\d+)$', id_url).group()

        img_path = os.path.join(self.img_path,query_txt+str(num)+'.jpg')

        urllib.request.urlretrieve('https://footsell.com' + img_url,img_path)

if __name__ == '__main__':
    soup_list = []

    target = 'https://footsell.com/'
    add_uri = r'g2/bbs/board.php?bo_table=m51&r=ok'

    fs = Make_driver()
    fs.driver.implicitly_wait(10)
    fs.driver.get(target + add_uri)
    fs.driver.refresh()
    fs.parser(soup_list)
    objs = fs.check(soup_list)
    obj = []

    app = create_app()
    with app.app_context():

        num = 1
        for title, condition, size, price, seller, uploadtime, uri, img in objs:
            obj.append(Shoes(title=title, condition=condition, size=size, price=price,
                             seller=seller, upload_date=uploadtime,
                             uri=uri, img=img))
            # 이미지 처리방식 변경필요
            # fs.save_img(img, num)
            num += 1
        db.session.bulk_save_objects(obj)
        db.session.commit()

    # num = 1
    # for title, condition, size, price, seller, uploadtime, uri, img in objs:
    #     obj.append(Shoes(title=title, condition=condition, size=size, price=price,
    #                      seller=seller, upload_date=uploadtime,
    #                      uri=uri, img=img))
    #     # 이미지 처리방식 변경필요
    #     # fs.save_img(img, num)
    #     num += 1

    # db.session.bulk_save_objects(obj)
    # db.session.commit()

    fs.driver.quit()
    del fs