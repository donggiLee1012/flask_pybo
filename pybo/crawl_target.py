from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os



class Make_driver:
    robots = 'robots.txt'
    driverpath = r'C:\projects\firstproject\pybo\static\chromedriver.exe'

    def __init__(self):
        self.driver = webdriver.Chrome(Make_driver.driverpath)


    def __call__(self,target):
        self.driver.get(target)

    def exit(self):
        self.driver.quit()