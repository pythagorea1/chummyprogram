# -*- coding:utf-8 -*-                                                                                                                                            
import urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
from urllib.parse import urlparse
import re
import json
import csv
from setting import *
from urllib.error import HTTPError,URLError
from time import sleep

html = urlopen("http://airbnb-japan.xyz/airbnb-daikou/airbnb-hikaku/")
bsObj = BeautifulSoup(html,"lxml")
listInTokyo = bsObj.find("th",{"id":"tokyo"}).parent

