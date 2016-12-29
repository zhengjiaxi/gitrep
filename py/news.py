# _*_ coding:utf-8 _*_
import re
import urllib2
import mysql.connector

key = raw_input(u'请输入年份：')
p = int(raw_input('请输入月份和日期：'))
strn1 = str(key)
strn2 = str(p)
url = r'http://www.chinanews.com/scroll-news/'+strn1+r'/'+strn2+r'/news.shtml'
socekt = urllib2.urlopen(url)
html = socekt.read()

#匹配新闻大段源代码，返回一个列表
news = re.findall(r'<div class="dd_lm">(.+?)</div></li>',html)

r1 = []
r2 = []
r3 = []
r4 = []


for news_code in news:
        
	#匹配新闻分类，返回一个列表
	news_category = re.findall(r'html>(.+?)</a>]</div>',news_code)
	r1.append(news_category[0])
	
	#匹配新闻标题和网址
	news_url_title = re.findall(r'<div class="dd_bt"><a href="(.+?)">(.+?)</a></div>',news_code)
	
	
	#匹配新闻网址处理，显示完整网址
	news_url = 'http://www.chinanews.com/'+news_url_title[0][0]
	r2.append(news_url[0])

	
	#匹配新闻标题处理
	news_title =  news_url_title[0][1]
	r3.append(news_title[0])

	
	#匹配新闻时间，返回一个列表
	news_time = re.findall(r'<div class="dd_time">(.+)',news_code)
	r4.append(news_time[0])
	

	zxx = zip(r1,r2,r3,r4)

	cnx = mysql.connector.connect(user='root',password='yhw919',host='127.0.0.1',database='chinanews')
	cursor = cnx.cursor ()
	add_rs = ('insert into zxx(category,url,title,ndate) valuse (%s,%s,%s,%s)')
	n=len(news_url)
	for j in range(n):
		try:
			cursor.execute(add_rs,zxx[j])
			cnx.commit()
		except Exception as e:
			print	e
			cnx.rollback()
	cursor.close()
	cnx.close
print u'录入信息成功'
