#coding:utf-8


from MySqlDBhelper import MySqlHelper
import hashlib

def user_register(name,passwd,helper):
	#用户注册
	sql = 'insert into users(name,passwd) values(%s,%s)'
	helper.cud(sql,[name,passwd])






def user_login(name,passwd,helper):
	#用户登录
	sql = "select passwd from users where name=%s"
	ret = helper.select(sql,[name])
	print('*'*10)
	print(ret)
	print('*'*10)
	if len(ret) == 0: 
		print('用户名错误')
		return
	elif ret[0][0] == passwd:
		print('登录成功')
	else:
		print('密码错误')
	
	
if __name__=='__main__':
	name = raw_input("输入用户名:")
	psw = raw_input("输入密码:")

	m = hashlib.sha1()
	m.update(psw)
	passwd = m.hexdigest()

	helper = MySqlHelper(host='localhost',user='root',passwd='231024',db='TestDB')
	#user_register(name,passwd,helper)
	user_login(name,passwd,helper)

