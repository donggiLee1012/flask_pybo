from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os, re, sys
import time as t
from datetime import *
import math
import urllib
import urllib.request
import requests



class Make_driver:

    #options = webdriver.ChromeOptions

    #
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome(driverpath,chrome_options=chrome_options)



    def __init__(self,target,query_txt='', size='', quantity=100):

        robots = 'robots.txt'

        # only window
        driverpath = os.path.join(os.path.dirname(__file__))
        driverpath += r'/chromedriver.exe'

        if target == 'xxblue':
            self.target = 'https://www.xxblue.com/'
        elif target == 'footsell':
            self.target = 'https://footsell.com/g2/bbs/board.php?bo_table=m51&r=ok'

        elif target =='bgjt':
            self.target = 'https://m.bunjang.co.kr/'
        else:
            pass

        # 사이즈
        if size == '':
            self.size = ''
        else:
            self.size = int(size)

        # 검색어
        if query_txt == '기본':
            self.query_txt = ''

        else:
            self.query_txt = query_txt

        # 수량
        self.quantity = int(quantity)

        # 리눅스 : 헤드리스 필수
        options = webdriver.ChromeOptions()
        # 전체화면
        options.add_argument('--start-fullscreen')
        self.driver = webdriver.Chrome(executable_path=driverpath, chrome_options=options)

        self.driver.implicitly_wait(10)
        self.driver.get(self.target)

        # 날짜 생성
        self.time_marker = datetime.now()

        # 이미지 저장경로
        self.img_path = r'C:\projects\firstproject\pybo\static\crawling_data\img\{}'.format(target)

        if os.path.exists(self.img_path):
            pass
        else:
            os.makedirs(self.img_path)

    def footsell_search(self):
        # 검색
        search_box = self.driver.find_element_by_css_selector('#list_search_text_input')
        search_box.send_keys(self.query_txt)
        search_box.send_keys(Keys.ENTER)

        # 사이즈별 선택한게있으면 실행
        if self.size != '':
            input_size = 'option[value="' + '{}"]'.format(self.size)
            size_select = self.driver.find_element(By.CSS_SELECTOR, input_size)
            size_select.click()


    def footsell_parser(self, soup_list=[]):

        for j in range(math.ceil(self.quantity / 40)):
            self.driver.implicitly_wait(10)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            border_list = soup.find_all(id=re.compile('list_row_'))

            if border_list == []:
                border_list = '결과안잡힘'
                soup_list.append(border_list)
                break

            if self.query_txt == '':
                border_list = border_list[3:]

            soup_list.append(border_list)

            try:
                self.driver.find_elements(By.CSS_SELECTOR, 'ul>li>a')[j].send_keys(Keys.ENTER)
            except:
                break



    def footsell_check(self, soup_list):
        title = []
        condition = []
        size = []
        price = []
        seller = []
        uploadtime = []
        uri = []
        img = []

        count = 0

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
                    # 금액
                    price_att = border_list_att.find('div', class_=re.compile('^list_market_price')).text.strip()
                    price_att = int(price_att[1:].replace(',',''))

                except AttributeError:
                    # 금액 0
                    price_att = 0

                except:
                    # 거래종료
                    price_att = border_list_att.find('span', class_='color_aaa normal smallfont').text.strip()
                    price_att = 0

                # 판매자명
                seller_att = border_list_att.find('div', class_=re.compile('^float_left list_market_name')).text.strip()

                # 업로드 시각
                uploadtime_att = border_list_att.find('span', class_='list_table_dates').text.strip()

                # uri
                uri_att = border_list_att.find('a').get('href')

                # img
                img_att = border_list_att.find('img').get('src')

                if ':' in uploadtime_att:
                    uploadtime_att = datetime.now()
                else:

                    uploadtime_att = datetime.strptime('20' + uploadtime_att, '%Y-%m-%d').date()

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

    def footsell_save_img(self, img_url):

        # b_id = re.search('(\d+)$', id_url).group()
        img_path = os.path.join(self.img_path,img_url[39:])
        urllib.request.urlretrieve('https://footsell.com' + img_url, img_path)

###################################### xxblue crawling ######################################

    def xxblue_search(self,query_txt):
        self.driver.find_element_by_css_selector('.search-btn').click()

        search = self.driver.find_element_by_name('keyword')

        search.send_keys(query_txt)

        search.send_keys(Keys.ENTER)
        # 첫번째 상품
        try:
            self.driver.find_elements_by_css_selector("div[class^='rarex-grid-product product']")[0].click()
        except:
            print('검색결과없음')

        self.driver.implicitly_wait(10)
        title=self.driver.find_element_by_css_selector('.product-subname').text
        img_name = self.driver.find_element_by_css_selector('.product-name').text.replace(' ','').lower()
        # 입찰 현황 더보기란 클릭
        # or driver.find_element_by_id('latestTransactionMore').click()
        self.driver.find_element_by_id('asknMore').click()
        t.sleep(0.5)

        # 거래가격 탭 클릭
        self.driver.find_element_by_css_selector('label[for="transactedPrice"]').click()

        uri = self.driver.current_url
        return title,uri,img_name

    def xxblue_element_generate(self):
        current =0
        while 1:
            table_td = self.driver.find_elements_by_css_selector('#transactedPriceTable tr')
            # ELEMENT 가 화면에 보이도록 스크롤 조정 --> 아래 부분 추가로 확장됨
            self.driver.execute_script("arguments[0].scrollIntoView(true);", table_td[-1])
            t.sleep(1)
            if current != len(table_td):
                current = len(table_td)
            else:
                break

    def xxblue_parser(self,objs=[]):
        objs = []

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        saledatas = soup.select('#transactedPriceTable tr')

        a = soup.find(class_='product-info').text
        shoesmodel_id = re.search('(스타일코드\s)(.*)(\s)',a).group(2)
        for i in saledatas:
            column = []
            for j in i.select('td'):
                column.append(j.text)
            objs.append(column)

        return objs,shoesmodel_id

###################################### xxblue end ######################################

###################################### bgjt crawling ######################################
    def bgjt_search(self):
        # 검색
        search = self.driver.find_element_by_css_selector('input[type="text"]')

        search.send_keys(self.query_txt)

        search.send_keys(Keys.ENTER)


    def bgjt_parser(self, soup_list=[]):

        for j in range(math.ceil(self.quantity / 40)):
            t.sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            t.sleep(1)
            salelist = soup.select("div[class$='fUCDDC']")

            if salelist == []:
                salelist = '결과안잡힘'
                soup_list.append(salelist)
                break

            soup_list.append(salelist)

            try:
                self.driver.find_elements_by_css_selector("a[class$='cAiauy']")[0].text
            except:
                break

    def bgjt_check(self, soup_list) :
        title = []
        condition = []
        size = []
        price = []
        seller = []
        uploadtime = []
        uri = []
        img = []
        count=0
        for soup_list_num in soup_list :
            for border_list in soup_list_num:
                # title
                title_att = border_list.find(class_=re.compile("dYmkxB$")).text
                print(title_att)

                # price
                try:
                    price_att = border_list.find(class_=re.compile("UVCRv$")).text.replace(',','')
                except:
                    # 연락요망
                    price_att = 0
                print(price_att)

                condition_att = '알수없음'
                size_att ='???mm'
                seller_att = '번개장터'

                # url
                uri_att = border_list.find(class_=re.compile("JQKtC$")).get('href')

                # date 광고이면 AD
                if border_list.find(class_=re.compile("dhsjSi")).text == 'AD':
                    uploadtime_att = '광고'
                else:
                    uploadtime_att = border_list.find(class_=re.compile("dhsjSi")).text

                # img
                img_att = border_list.find("img", alt="상품 이미지").get('src')

                if uploadtime_att == '광고' :
                    uploadtime_att = self.time_marker

                elif '일' in uploadtime_att:
                    day = re.match('\d+', uploadtime_att).group()
                    uploadtime_att = self.time_marker - timedelta(days=int(day))

                elif '시간' in uploadtime_att:
                    hour = re.match('\d+', uploadtime_att).group()
                    uploadtime_att = self.time_marker - timedelta(hours=int(hour))

                elif '주' in uploadtime_att:
                    week = re.match('\d+', uploadtime_att).group()
                    uploadtime_att = self.time_marker - timedelta(weeks=int(week))
                elif '월' in uploadtime_att:
                    month = re.match('\d+', uploadtime_att).group()
                    uploadtime_att = self.time_marker - timedelta(days=int(month)*30)

                else:
                    uploadtime_att = self.time_marker

                print(uploadtime_att)

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



