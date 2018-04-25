#coding:utf-8

from MySQLdb import *

class MySqlHelper(object):
	def __init__(self,db,user,passwd,host='localhost',port=3306,charset='utf8'):
		self.charset=charset
		self.host=host
		self.port=port
		self.user=user
		self.passwd=passwd
		self.db=db
	

	def open(self):
		self.conn = connect(host=self.host,port=self.port,charset=self.charset,db=self.db,
							user=self.user,passwd=self.passwd)
		self.cursor = self.conn.cursor()
	
	def close(self):
		self.cursor.close()
		self.conn.close()
	


	def cud(self,sql,params):
		try:
			self.open()
			self.cursor.execute(sql,params);
			
			self.conn.commit()
			self.close()
			print('OK!')
		except Exception,e:
			print(e.message)
	
	def select(self,sql,params=[]):
		try:
			self.open()
			self.cursor.execute(sql,params)
			result = self.cursor.fetchall()
			self.close()
			return result
		except Exception,e:
			print(e.message)


if __name__ == '__main__':
	dbhelper = MySqlHelper(host='localhost',db='TestDB',user='root',passwd='231024')

	#name = raw_input("请输入姓名:")
	#stuid = int(raw_input("请输入学生id:"))
	#print(type(stuid))
	#params=[name,stuid]
	#sql="update student set name=%s where id=%s"
	#dbhelper.cud(sql,params)

	sql = 'select * from student'
	ret = dbhelper.select(sql)
	print(ret)

