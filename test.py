import urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request

site= "https://www.airbnb.jp/"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
html = urlopen(req)
bsObj = BeautifulSoup(html,"html.parser")
example = bsObj.find("a",{"class":"screen-reader-only screen-reader-only-focusable skip-to-content"}).get_text()
print(example)
