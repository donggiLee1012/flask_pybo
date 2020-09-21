from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os,time

from flask import Blueprint, url_for, request, render_template,g,flash
from ..crawl_target import Make_dirver

bp = Blueprint('shoes',__name__,url_prefix='/shoes')

@bp.route('/main')
def main():
    target = 'https://footsell.com/'
    add_uri = r'g2/bbs/board.php?bo_table=m51&r=ok'

    footsell = Make_dirver(target+add_uri)

    form = type(footsell)


    return render_template('shoes/main.html',form=form)
