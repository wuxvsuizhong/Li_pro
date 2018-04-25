import time

# /ctime.py?timezone=e8
# /ctime.py?timezone=e1


def application(env,start_response):
	#用户所有的请求数据都放在env中
	#HTTP头相关的内容
	env.get("METHOD","")
	env.get("PATH_INFO","")
	env.get("QUERY_STRING","")


	status = "200 OK"
	headers = [ 
		("Content-Type","text/plain")
	]

	start_response(status,headers)#一方面通过start_response传递出响应头
	return time.ctime()#一方面return出相应数据体


