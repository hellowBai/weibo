import requests
import re
import os
import json
from bs4 import BeautifulSoup

class WbGrawler():
    def __init__(self,url):
        """
        参数的初始化
        :return:
        """
        self.baseurl = url
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "cookie":"SINAGLOBAL=1282576536686.5537.1548081285406; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWjgq.FGzv-Eav0UIoDDXUv5JpX5KzhUgL.Fo-4S02cSonE1Kq2dJLoIEBLxK-L1h-L1h.LxK-LB.BLBo2LxK-LB.-LB--LxKMLB.-LB.Bt; SUHB=0TPVr0nXkhFeEi; login_sid_t=57132aa4e80a9a7c6e06ecbd94aa2ab2; cross_origin_proto=SSL; YF-V5-G0=4e19e5a0c5563f06026c6591dbc8029f; _s_tentry=-; Apache=2848923951780.724.1577848651863; ULV=1577848651910:4:1:1:2848923951780.724.1577848651863:1577359929079; ALF=1609384722; SSOLoginState=1577848724; wvr=6; YF-Page-G0=e57fcdc279d2f9295059776dec6d0214|1577848984|1577848730; UOR=cn.bing.com,www.weibo.com,login.sina.com.cn; WBStorage=42212210b087ca51|undefined; Ugrow-G0=5c7144e56a57a456abed1d1511ad79e8; wb_view_log_5971668296=1408*7921.3636363636363635; webim_unReadCount=%7B%22time%22%3A1577849011654%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A7%2C%22msgbox%22%3A0%7D",
            "referer": "https://www.weibo.com/u/5644764907?topnav=1&wvr=6&topsug=1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
        }
        # 图片保存路径
        self.path = "D:/weibosrc/"


def getPageJson(self, page):
    """
    获取单个页面的json数据
    :param page:传入的page参数
    :return:返回页面响应的json数据
    """
    url = self.baseurl + "page=%d" % page
    print(url)
    try:
        response = requests.get(url, self.headers)
        print(response.content.decode("gbk").jsonlode())
     #   if response.status_code == 200:
     #       return response.json()
    except requests.ConnectionError as e:
        print("error", e.args)