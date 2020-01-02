from Include import def_pic

import requests
import re
import os
from bs4 import BeautifulSoup
import  urllib3
import json
from time import sleep

def main():
    url='https://weibo.com/u/'
    host='rm.weibo.cn'


    pic=def_pic.WbGrawler(url)
    def_pic.getPageJson(pic,1742727537)

    """
     html=def_pic.def_pic(url)
    htmlLine = html.text.splitlines()
    data=html.content.decode('gbk')
    dataLine=data.splitlines()
    for row in dataLine:
         print(row)
    
    """


if __name__=='__main__':
    main()