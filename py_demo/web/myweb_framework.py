import time
import dynamic_web_server
import sys

WSGI_PYTHON_DIR = "./wsgipython/"
STATIC_DIR = "."
''''
def application(env,start_respornse):
	urls = [
		("/ctime",show_ctime),
		("/sayhello",say_hello)
	]





	status = "200 OK"
	headers = [
		("Content-Type":"text/plain")
	]
	start_respomse(status,headers
	return time.ctime()
'''

def show_ctime(env,start_response):
	status = "200 OK"
	headers = [
		("Content-Type","text/plain"),
	]
			
	dynamic_web_server.start_response(status,headers)
	return time.ctime()

def say_hello(env,start_response):
	status = "200 OK"
	headers = [
		("Content-Type","text/plain"),
	]
	dynamic_web_server.start_response(status,headers)
	return "hello!"

def say_haha(env,start_response):
	status = "200 OK"
	headers = [
		("Content-Type","text.plain"),
	]
	start_response(status,headers)
	return "Haha Haha!"


#客户请求与处理函数映射列表
urls = [
	("/ctime",show_ctime),
	("/sayhello",say_hello),
	("/sayhaha",say_haha),
]


class Application(object):
	def __init__(self,urls):
		'''
		获取并设置路由信息
		'''
		self.urls = urls
	
	def __call__(self,env,start_response):
		path = env.get("PATH_INFO","/")#获取请求文件的路径
		print("Application--- path = %s"%(path))
		if path.startswith("/static"):#请求以static开头，那么是静态文件
			path = path[7:]#截掉/static开头
			path = STATIC_DIR + path
			try:
				with open(path,'r') as file_data:
					data = file_data.read()
					file_data.close()
					status = "200 OK"
					headers = []
					return data	#返回读取的静态文件
			except IOError:
				status = "404 Not Found"
				headers = []
				dynamic_web_server.start_response(status,headers)
				return "not found"

		for url,handler in self.urls:
			if path  == url:#如果有url和用户请求匹配
				return  handler(env,start_response)
		#没找到匹配,返回404		
		status = "404 Not Found"
		headers = []
		dynamic_web_server.start_response(status,headers)
		return "not found"



def main():
	sys.path.insert(1,WSGI_PYTHON_DIR)
	app = Application(urls)
	dynamic_web_server.main(app)



if __name__ == '__main__':
	main()
