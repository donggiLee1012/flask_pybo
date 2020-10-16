import sqlite3
from templates.modules.crawl_target import Make_driver
import os
import time

if __name__ =='__main__':
    BASE_DIR = os.path.join(os.path.join(os.path.pardir,'pybo.db'))

    db = sqlite3.connect(BASE_DIR)
    soup_list = []

    target = 'https://www.xxblue.com/'

    xb = Make_driver()
    xb.driver.implicitly_wait(10)
    xb.driver.get(target)

    xb.driver.find_element_by_css_selector('.search-btn').click()

    xb.xxblue_search()
    # search = xb.driver.find_element_by_name('keyword')
    # keyword = 'B75571'
    # search.send_keys(keyword)
    #
    # search.send_keys(xb.Keys.ENTER)

    # 첫번째 상품
    try:
        xb.driver.find_elements_by_css_selector("div[class^='rarex-grid-product product']")[0].click()
    except:
        print('검색결과없음')

    # 입찰 현황 더보기란 클릭
    # or driver.find_element_by_id('latestTransactionMore').click()
    xb.driver.find_element_by_id('asknMore').click()

    # 거래가격 탭 클릭
    xb.driver.find_element_by_css_selector('label[for="transactedPrice"]').click()

    current = 0



    while 1:
        table_td = xb.driver.find_elements_by_css_selector('#transactedPriceTable tr')
        # ELEMENT 가 화면에 보이도록 스크롤 조정 --> 아래 부분 추가로 확장됨
        xb.driver.execute_script("arguments[0].scrollIntoView(true);", table_td[-1])
        time.sleep(1)
        if current != len(table_td):
            current = len(table_td)
            print(current)
        else:
            break


    soup = xb.xxblue_parser()

    xb.driver.quit()

    saledatas = soup.select('#transactedPriceTable tr')

    row = []

    for i in saledatas:
        column = []
        for j in i.select('td'):
            column.append(j.text)
        row.append(column)

    print(row)