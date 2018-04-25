#coding:utf-8

from MySQLdb import *

try:
	conn = connect(host='localhost',user='root',passwd='231024',charset='utf8',db='TestDB')	
	cursor = conn.cursor()
	names = raw_input("输入姓名:")	
	sql="insert into student(name) values(%s)"
	cursor.execute(sql,[names])
	conn.commit()


	cursor.close()
	conn.close()

except Exception, e:
	print(e.message)
