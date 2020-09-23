from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os,time,re
import math
from flask import Blueprint, url_for, request, render_template,g,flash
from pybo.models import User
from werkzeug.utils import redirect
from ..crawl_target import Make_driver

from ..forms import SearchShoes

bp = Blueprint('shoes',__name__,url_prefix='/shoes')

@bp.route('/main/',methods=('GET','POST'))
def main():

    form = SearchShoes()

    if request.method == 'POST' and form.validate_on_submit():

        return render_template('shoes/shoes_result.html',method='POST',form=form)
    else:
        return render_template('shoes/main.html',form=form)



@bp.route('/footsell',methods=('GET','POST'))
def footsell(form):



    size = form.size.label
    query_txt = form.content.data



    target = 'https://footsell.com/'
    add_uri = r'g2/bbs/board.php?bo_table=m51&r=ok'
    
    fs = Make_driver()
    fs(target+add_uri)
    search(fs.driver,query_txt,size)

    # fs.driver.get('https://footsell.com/')
    return render_template('shoes/shoes_result.html',form=form)

@bp.route('/footsell/detail', methods=['POST'])
def footsell_detail():
    return 4


def search(driver,query_txt,size):
    # 검색
    search_box = driver.find_element_by_css_selector('#list_search_text_input')
    search_box.send_keys(query_txt)
    search_box.send_keys(Keys.ENTER)

    # 사이즈별 선택한게있으면 실행
    if size !='':
        input_size = 'option[value="' + '{}"]'.format(size)
        size_select = driver.find_element(By.CSS_SELECTOR, input_size)
        size_select.click()


def parser(driver,many=120,soup_list=[]):

    for j in range(math.ceil(int(many) / 40)):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(2)
        border_list = soup.find_all(id=re.compile('list_row_'))

        if border_list == []:
            print('검색결과없음')
            break

        soup_list.append(border_list)

        try:
            driver.find_elements(By.CSS_SELECTOR, 'ul>li>a')[j].send_keys(Keys.ENTER)
        except:
            break

def check(border_list_att):
    # 제목
    try:
        title = border_list_att.find('span', id=re.compile('^list_subject_')).text.strip()

    except:
        title = border_list_att.find('span', class_='smallfont color_aaa').text.strip()

    # 컨디션
    condition = border_list_att.find('span', class_='list_market_used han').text

    # 사이즈
    size = border_list_att.find('span', class_='list_market_size').text

    # 가격
    try:
        price = border_list_att.find('div', class_=re.compile('^list_market_price')).text.strip()
    except:
        price = border_list_att.find('span', class_='color_aaa normal smallfont').text.strip()

    # 판매자명
    seller = border_list_att.find('div', class_=re.compile('^float_left list_market_name')).text.strip()

    # 업로드 시각
    uploadtime = border_list_att.find('span', class_='list_table_dates').text.strip()

    # uri
    uri = border_list_att.find('a').get('href')

    # img
    img = border_list_att.find('img').get('src')

    if ':' in uploadtime:
        uploadtime = 1#Footsell.time_marker

    return [title, condition, size, price, seller, uploadtime, uri, img]

