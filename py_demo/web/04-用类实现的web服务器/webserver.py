from socket import *
from multiprocessing import Process
import re
import sys

APP_PATH = "."



class server(object):

	def __init__(self,port,app):
		self.sockconfig = ("",port)
		self.app = app
		self.response_header = ""
		try:
			self.listensock = socket(AF_INET,SOCK_STREAM)
			self.listensock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
			self.listensock.bind(self.sockconfig)
		except:
			print("socket error")

	def start_response(self,status,headers):
		self.response_header = "HTTP/1.1 " + status + "\r\n"
		for each in headers:
			self.response_header += "%s:%s\r\n"%each


	def do_server(self,clientsock,clientinfo):
		recv_data = clientsock.recv(1024).decode('utf-8')
		if 0 == len(recv_data):
			return
		request_lines = recv_data.splitlines()
		for each_line in request_lines:
			print(each_line)
		
		file_name = re.match(r"\w+ +(/[^ ]*) ",request_lines[0]).group(1)
		print("file_name = %s"%file_name)
		env = { 
			"PATH_INFO":file_name,
			"method":"",
		}
		response_body = self.app(env,self.start_response)	
		res_type = self.response_header[0].split("/")
		print("res_type = %s"%str(res_type))
		#esponse_body = response_body.encode('utf-8')	
		response_data = self.response_header.encode('utf-8') + "\r\n" + response_body
		#print("response_data = %s"%(response_data))

		ret = clientsock.send(response_data)
		print("ret = %d"%ret)
		clientsock.close()	
		


	def start(self):
		self.listensock.listen(100)
		while True:
			tmpclientsock,clientinfo = self.listensock.accept()
			client_P = Process(target = self.do_server,args = (tmpclientsock,clientinfo))
			client_P.start()
			tmpclientsock.close()
		self.listensock.close()


def main():
	#python3  webserver.py MyWebFramework:app
	module_name,app_name = sys.argv[1].split(":")
	m = __import__(module_name)#导入框架模块
	app=getattr(m,app_name)#导入框架的app名
	s = server(8080,app)
	s.start()
	

if __name__ == '__main__':
	main()
