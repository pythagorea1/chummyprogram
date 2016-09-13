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

def toHex(n):
	if n < 10:
		return str(n)
	else:
		return chr(ord("A")+n-10)
def toUnicodeEscape(s):
	out = ""
	b = s.encode()
	for i in range(0, len(b)):
		out += "%" + toHex(b[i] // 16) + toHex(b[i] % 16)
	return out

def getValue(responseJson, name, number):
	try:
		hoge = responseJson.get(name)
	except IndexError:
		pass
	else:
		if hoge != None:
			return hoge[number].get("value")

def getWhatYouNeed(responseJson,names):
	ans = responseJson
	if ans == None:
		return None
	for name in names:
		ans = ans.get(name)
		if ans == None:
			return None
	return ans

def setValue(info, key, val):
	if val != None:
		info[key] = val

hdr = {'User-Agent': 'Mozilla/5.0'}

def getInfo(link):
	try:
		req2 = Request(link,headers=hdr)
		html = urlopen(req2)
	except (HTTPError,URLError) as e:
		print(e)
		return None
	bsObj2 = BeautifulSoup(html,"html.parser")
	data=urlopen(req2).read()
	jsonFiles = bsObj2.findAll("script",{"type":"application/json"})
	num=0
	info=default.copy()
	info["url"] = link
	for jsonFile in jsonFiles:
		s = str(jsonFile)
		f = s[s.find("{") : s.rfind("}") + 1]
		num += 1
		responseJson = json.loads(f)
		for key in howto.keys():
			setValue(info,key,getWhatYouNeed(responseJson,howto[key]))
	length = len(info["review_summary"])
	lengthOfAmenities = len(info["listing_amenities"])
	for i in range(0,length):
		hoge = info["review_summary"][i]
		if hoge != None:
			info[review[i]] = info["review_summary"][i].get("value")
	
	for i in range(0,lengthOfAmenities):
		hoge = info["listing_amenities"][i]
		if hoge != None:
			info[hoge.get("tag")] = hoge.get("is_present")
				
	info["cleaning_fee"] = info["cleaning_fee"].replace("&amp;yen; ","￥")
	info["extra_people"] = info["extra_people"].replace("&amp;yen; ","￥")
		
	return info
			

SetOfRooms = set()
SetOfLocations = set()
while True:
	print("検索したい場所は? (例 : 東京, ローマ字も可能) : ",end="")
	location = input()
	SetOfLocations.add(location)
	if location == "end":
		break;
	
while True:
	print("何件くらい取得したいですか? (例 : 300) : ",end="")
	number = input()
	if re.match("^[0-9]*$",number) != None:
		number = (int(number)+17)//18
		break

while True:
	print("保存名 (例 : AirbnbInTokyo, 半角英数字のみ) : ",end="")
	locationName = input()
	if re.match("^[a-zA-Z0-9]*$",locationName) != None:
		break
infos = []
for location in SetOfLocations:
	if location == "end":
		pass
	else:
		for x in range(0,number):
			site= "https://www.airbnb.jp/s/"+toUnicodeEscape(location)+"?guests=1&page="+str(x)
			req = Request(site,headers=hdr)
			try:
				html = urlopen(req)
			except (HTTPError,URLError) as e:
				print(e)
				pass
			else:
				bsObj = BeautifulSoup(html,"html.parser")
				roomUrls = bsObj.findAll("a",href = re.compile("^(/rooms/)((?![a-z]).)*"))
				for link in roomUrls:
					hrefOfRoom = link.attrs['href']
					if re.match("(^/rooms/)((?![a-z]).)*",hrefOfRoom).group() != "/rooms/":
						if hrefOfRoom not in SetOfRooms:
							SetOfRooms.add(hrefOfRoom)
							print("https://www.airbnb.jp"+hrefOfRoom)

numOfLink = len(SetOfRooms)
print(str(numOfLink) + " 件発見しました.")
print("情報を取得します...")
processingNum = 0
for link in SetOfRooms:
	processingNum+=1
	processingRate = processingNum/numOfLink
	print("https://www.airbnb.jp"+link,"進行度 : {:.2%}".format(processingRate))
	for i in range(0, 3):
		info = getInfo("https://www.airbnb.jp"+link)
		if info != None:
			infos.append(info)
			break
		else:
			print("エラー! リトライします.")
			sleep(2)
		

print(str(len(SetOfRooms)) + " 件取得しました.")
csvFile = open(locationName+".csv","w+",newline="",encoding = 'utf-16')
try:
	writer = csv.writer(csvFile)
	writer.writerow(tuple(ks))
	for i in range(len(infos)):
		writer.writerow(tuple(map(lambda x: '"' + str(infos[i][x]) + '"' if x in string else infos[i][x], ks)))
finally:
	csvFile.close()
