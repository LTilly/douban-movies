'''
		将清洗后的电影信息存入数据库
'''

import json
import pymysql

# 连接数据库
db=pymysql.connect(host='127.0.0.1', user='root', passwd='456789', db='douban', port=3306, charset='utf8', cursorclass = pymysql.cursors.DictCursor)
db.autocommit(True)
cursor=db.cursor()

# 获取清洗后的电影信息
f=open('cleanedMovie.json','r')
movies=json.load(f)
f.close()

# 将每部电影的信息逐条存入数据库
for mov in movies:
	cursor.execute('insert into movies(id,title,rate,url,cover,director,composer,actor,category,district,language,name,time,length,description) \
		values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',\
		[mov['id'],mov['title'],mov['rate'],mov['url'],mov['cover'],mov['director'],mov['composer'],mov['actor'],\
		mov['category'],mov['district'],mov['language'],mov['name'],mov['time'],mov['length'],mov['description']])

# 关闭数据库连接
cursor.close()
db.close()