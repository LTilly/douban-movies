'''
		做一些简单的数据统计，用于减少网页请求数据库的次数
'''

import json
import pymysql

# 获取清洗后的电影数据
f=open('cleanedMovie.json','r')
movies=json.load(f)
f.close()

# 用于语言名称统一的字典
langMap = {}
langMap['中文'] = '汉语普通话'
langMap['国语'] = '汉语普通话'
langMap['普通话'] = '汉语普通话'
langMap['english'] = '英语'
langMap['English'] = '英语'
langMap['无声'] = '无对白'
langMap['Tibetan'] = '藏语'
langMap['Icelandic'] = '冰岛语'
langMap['Klingon'] = '克林贡语'
langMap['Shanghainese'] = '上海话'
langMap['Hawaiian'] = '夏威夷语'
langMap['Belarusian'] = '白俄罗斯语'
langMap['四川方言'] = '四川话'
langMap['Swahili'] = '斯瓦希里语'
langMap['Assyrian'] = '亚述语'
langMap['古代英语'] = '古英语'
langMap['福建话'] = '闽南语'
langMap['闽南话'] = '闽南语'
langMap['俄罗斯语'] = '俄语'
langMap['韩国语'] = '韩语'
langMap['法国'] = '法语'
langMap['西班牙'] = '西班牙语'
langMap['捷克'] = '捷克语'
langMap['Galician'] = '加利西亚语'
langMap['Inuktitut'] = '因纽特语'
langMap['东北方言'] = '东北话'
langMap['陕西方言'] = '陕西话'
langMap['武汉方言'] = '武汉话'
langMap['Sicilian'] = '西西里语'
langMap['Serbian'] = '塞尔维亚语'
langMap['Punjabi'] = '旁遮普语'

# 定义字典用于存储统计结果
categories={}
districts={}
languages={}
times={}
lengths={}
rates={}
combined={}

# 统计中用到的简易计数函数
def count(item,dct):
	if item not in dct:
		dct[item]=1
	else:
		dct[item]+=1

# 数据统计
for mov in movies:
	# 统计各国各类电影的评分
	if mov['district']!='' and mov['category']!='':
		for d in mov['district'].split('/'):
			d=d.split('_')[0]
			if d not in combined:
				combined[d]={}
			for c in mov['category'].split('/'):
				if c not in combined[d]:
					combined[d][c]={'avg':0.0,'cnt':0}
				combined[d][c]['avg']=(combined[d][c]['avg']*combined[d][c]['cnt']+float(mov['rate']))/(combined[d][c]['cnt']+1)
				combined[d][c]['cnt']+=1

	# 类型统计
	if mov['category']!='':
		for item in mov['category'].split('/'):
			count(item,categories)

	# 地区统计
	if mov['district']!='':
		for item in mov['district'].split('/'):
			item=item.split('_')[0]
			count(item,districts)

	# 语言统计
	if mov['language']!='':
		for item in mov['language'].split('/'):
			item=item.split(' ')[0]
			# 统一语言名
			if item in langMap:
				item=langMap[item]
			count(item,languages)

	# 上映日期统计
	if mov['time']!='0':
		count(mov['time'],times)

	# 片长统计
	if mov['length']!='0':
		count(mov['length'],lengths)

	# 评分统计
	count(mov['rate'],rates)

# 连接数据库
db=pymysql.connect(host='127.0.0.1', user='root', passwd='456789', db='douban', port=3306, charset='utf8', cursorclass = pymysql.cursors.DictCursor)
db.autocommit(True)
cursor=db.cursor()

# 将各国各类电影的评分数据存入数据库
comb={}
for key,val in combined.items():
	comb[key]={}
	cat=''
	rat=''
	for k,v in val.items():
		cat=cat+k+','
		rat=rat+'%.3f' % v['avg'] +','
	comb[key]['categories']=cat[:-1]
	comb[key]['rates']=rat[:-1]
	cursor.execute("insert into rate(district,categories,rates) values(%s,%s,%s)",[key,cat[:-1],rat[:-1]])

# 关闭数据库连接
db.close()
cursor.close()

print(str(comb))
print(str(categories))
print(str(districts))
print(str(languages))
print(str(times))
print(str(lengths))
print(str(rates))
