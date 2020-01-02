import re
import requests
from bs4 import BeautifulSoup

pat=re.compile('http://+[a-zA-Z0-9\./]+')
url ='https://weibo.com/'


html=requests.get(url)
html.encoding='gdk'
htmlLine=html.text.splitlines()

m=pat.findall(html.text)
#print(m)

for row in htmlLine:
    print(row)



#抓取网页
sp=BeautifulSoup(html.text,"html.parser")

