#coding:utf-8


from redis import *
from MySqlDBhelper import MySqlHelper
import hashlib

def login():
	name = raw_input('输入姓名:')
	pwd = raw_input('输入密码:') 
	m = hashlib.sha1()
	m.update(pwd)
	passwd = m.hexdigest()

	#先在redis里面查询
	r = StrictRedis(host='127.0.0.1',port=6379)
	redis_sel_ret = r.get(name)
	#print(redis_sel_ret)

	if redis_sel_ret is None:
		sel_result = sel_mysql(name)
		#没有找到再到mysql里面查询
		if len(sel_result) == 0:
			print('用户不存在!')
			return None
		elif sel_result[0][0] == passwd:
			print('登录成功!----on mysql')
			#mysql登录成功后把数据加到redis里面
			r.setex(name,60,passwd)
			return 0
		else:
			print('密码错误!')
			return -1
	elif redis_sel_ret  == passwd:
		#redis里面能查到信息
		print('登录成功!----on redis')
		return 0
	else:
			print('密码错误!')
			return -1

def register():
	name = raw_input('输入姓名:')
	pwd = raw_input('输入密码:') 
	if pwd != raw_input('再次输入密码:'):
		print('密码不一致!')
		return -1
		
	m = hashlib.sha1()
	m.update(pwd)
	passwd = m.hexdigest()

	r = StrictRedis(host='127.0.0.1',port=6379)
	r.setex(name,300,passwd)
	#添加到mysql中
	mysql_helper = MySqlHelper(host='localhost',user='root',passwd='231024',db='TestDB')
	sql = "insert into users (name,passwd) values(%s,%s)"
	mysql_helper.cud(sql,[name,passwd])
	


def sel_mysql(name):
	mysql_helper = MySqlHelper(host='localhost',user='root',passwd='231024',db='TestDB')
	sql = 'select passwd from users where name=%s'
	ret = mysql_helper.select(sql,[name])#查询成功返回元组，没找到返回空元组
	return ret

if __name__ == '__main__':
	#login()
	opt = [login,register]
	choice = int(raw_input("1.登录\n2.注册\n"))
	opt[choice-1]()
