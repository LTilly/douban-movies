'''
		网页框架
'''

import pymysql
import json
from flask import Flask,url_for,render_template,request

app = Flask(__name__)
app.config.from_object(__name__)

# 连接数据库的函数
def connectdb():
	db=pymysql.connect(host='127.0.0.1', user='root', passwd='456789', db='douban', port=3306, charset='utf8', cursorclass = pymysql.cursors.DictCursor)
	db.autocommit(True)
	cursor=db.cursor()
	return (db,cursor)

# 关闭数据库的函数
def closedb(db,cursor):
	db.close()
	cursor.close()

# 首页/统计页面
@app.route('/')
def index():
	return render_template('index.html')

# 评分页面
@app.route('/rate/')
def rate():
	(db,cursor)=connectdb()
	cursor.execute("select rate,district,category,time,length from movies")
	movies=cursor.fetchall()
	temp=[]
	for mov in movies:
		if mov['district']!='' and mov['category']!='' and mov['time']>=1920 and mov['length']!=0 and mov['length']<=300:
			temp.append(mov)
	movies=json.dumps({"movies":temp})
	cursor.execute("select * from rate")
	rates=cursor.fetchall()
	temp={}
	for rat in rates:
		temp[rat['district']]={}
		temp[rat['district']]['categories']=rat['categories'].split(',')
		array=rat['rates'].split(',')
		temp[rat['district']]['rates']=[]
		for x in array:
			temp[rat['district']]['rates'].append(float(x))
	rates=json.dumps({"rates":temp})
	closedb(db,cursor)
	categories=['剧情','悬疑','惊悚','犯罪','战争','喜剧','动作','科幻','传记','运动','奇幻','冒险','家庭','爱情',\
	'儿童','歌舞','恐怖','动画','历史','灾难','情色','古装','音乐','同性','武侠','西部','黑色电影','脱口秀','鬼怪']
	districts=['Argentina', 'Armenia', 'Australia', 'Austria', 'Belgium', 'Bhutan', 'Botswana', 'Brazil',\
	'Bulgaria', 'Canada', 'Chile', 'China', 'Colombia', 'Cuba', 'Czech Republic', 'Denmark', 'Estonia',\
	'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',\
	'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg', 'Malaysia',\
	'Mexico', 'Myanmar', 'Netherlands', 'New Zealand', 'Norway', 'Panama', 'Philippines', 'Poland', 'Portugal',\
	'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain',\
	'Sweden', 'Switzerland', 'Tajikistan', 'Thailand', 'The Bahamas', 'Tunisia', 'Turkey', 'Ukraine',\
	'United Arab Emirates', 'United Kingdom', 'United States of America', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vietnam']
	return render_template('rate.html',movies=movies,rates=rates,categories=categories,districts=districts)

# 搜索页面
@app.route('/search/', methods=['GET','POST'])
def search():
	(db,cursor)=connectdb()
	cursor.execute("select * from movies order by rate desc limit 10")
	movies=cursor.fetchall()
	for mov in movies:
		mov['composer']=mov['composer'].replace('/',' ')
		mov['actor']=mov['actor'].replace('/',' ')
		mov['category']=mov['category'].replace('/',' ')
		mov['language']=mov['language'].replace('/',' ')
		mov['name']=mov['name'].replace('/',' ')
		temp=mov['district'].split('/')
		s=''
		for x in temp:
			s=s+x.split('_')[0]+' '
		mov['district']=s[:-1]
		mov['description']=mov['description'].split('\n')
	closedb(db,cursor)
	if request.method=='GET':
		return render_template('search.html',movies=movies,results=())
	else:
		# POST请求是因为用户提交了搜索的关键字
		keyword=request.form.get('keyword')
		(db,cursor)=connectdb()
		cursor.execute("select * from movies where title like '%%%s%%' order by rate desc" %keyword)
		results=cursor.fetchall()
		for mov in results:
			mov['composer']=mov['composer'].replace('/',' ')
			mov['actor']=mov['actor'].replace('/',' ')
			mov['category']=mov['category'].replace('/',' ')
			mov['language']=mov['language'].replace('/',' ')
			mov['name']=mov['name'].replace('/',' ')
			temp=mov['district'].split('/')
			s=''
			for x in temp:
				s=s+x.split('_')[0]+' '
			mov['district']=s[:-1]
			mov['description']=mov['description'].split('\n')
		closedb(db,cursor)
		return render_template('search.html',movies=movies,results=results,key=keyword)

if __name__=='__main__':
	app.run()