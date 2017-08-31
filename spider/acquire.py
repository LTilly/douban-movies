'''
		爬取豆瓣部分电影的概要信息
'''

import requests
import re
import json
from bs4 import BeautifulSoup

# 获取tag
url='https://movie.douban.com/j/search_tags?type=movie'
tags=requests.get(url,timeout=20).json()['tags']

# set用于避免重复，movies用于存放电影信息
s=set()
movies=[]
# 获取每部电影部分信息和URL
for tag in tags:
	limit=0
	while 1:
		#通过URL进入其中一页电影记录
		url='https://movie.douban.com/j/search_subjects?type=movie&tag='+tag+'&page_limit=20&page_start='+str(limit)
		res=requests.get(url,timeout=20).json()['subjects']

		# 判断该tag电影是否获取完毕
		if len(res)==0:
			break

		# 获取本页中的电影部分信息及URL
		limit+=20
		for item in res:
			if item['id'] in s:
				continue
			s.add(item['id'])
			movies.append(item)

# 剩余部分概要信息的标签
lst=['导演','编剧','主演','类型','制片国家/地区','语言','上映日期','片长','又名']
# 获取电影剩下的需要的概要信息
for x in range(0,len(movies)):
	item=movies[x]
	# 删除不要的信息
	del item['cover_x'],item['cover_y'],item['playable'],item['is_new']
	# 获取每个电影页面的HTML
	res=requests.get(item['url'],timeout=20).content.decode()
	soup=BeautifulSoup(res,"html.parser")

	try:
		# 找到HTML中存放的信息部分
		info=soup.select_one('#info').text.split('\n')

		# 判断每条信息是否需要，如需要则存储
		for y in range(1,len(info)-1):
			string=info[y].split(':',1)[0].strip()
			if string in lst:
				z=lst.index(string)
				item[lst[z]]=info[y].split(':',1)[1].strip()

		# 判断简介是否有隐藏内容，分两种情况获取简介
		if soup.select_one('.all'):
			des=soup.select_one('.all')
		else:
			des=soup.select('#link-report > span')[0]
		# 初步调整简介格式
		item['description']=re.sub('\s\s+','\n',des.text.strip())
	# 如发生错误记录错误信息（实际运行结果中只有一种错误，是由于简介不存在造成的）
	except Exception as e:
		print(e)
		print("xxx"+str(x))

# 将结果存在json中
f=open('movie.json','w')
json.dump(movies,f)
f.close()
