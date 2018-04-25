#可执行py脚本的web服务器

from socket import *
from multiprocessing import Process
import sys 
import re






HTTP_ROOT_DIR = "."
#WSGI_PYTHON_DIR = "./wsgipython/"

def main(app):
	appinfo = app 
	#创建socket
	s = socket(AF_INET,SOCK_STREAM)
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)#设置地址可重用
	try:
		s.bind(("",8080))
	except OSError as err:
		print('please wait %s'%str(err))
		sys.exit()
	#sys.path.insert(1,WSGI_PYTHON_DIR)#添加服务器端服务脚本路径到python找包路径

	s.listen(100)
	while True:
		client_sock,client_info = s.accept()
		print('new connection%s'%str(client_info))
		client_Process = Process(target = doserver,args=(client_sock,client_info,appinfo))
		client_Process.start()
		client_sock.close()		
	s.close()


response_head = ""

def start_response(status_code,res_headers):
	response_head = "HTTP/1.1"+status_code + "\r\n"
	for each in res_headers:
		response_head += "%s:%s\r\n"%each 
	

def doserver(client_sock,client_info,appinfo):
	#接受数据
	recv_data = client_sock.recv(2048)
	if len(recv_data) == 0:
		client_sock.close()
		return
	recv_data = recv_data.decode('utf-8')
	print(">>%s"%str(recv_data))
	#解析HTTP头
	data_list = recv_data.splitlines()

	#提取请请求路径
	request_start_line = data_list[0]
	file_name = re.match(r"\w+ +(/[^ ]*) ",request_start_line).group(1)
	method = re.match(r"(\w+) +/[^ ]* ",request_start_line).group(1)
	print('request file mame is %s'%str(file_name))

	env = {
		"PATH_INFO":file_name,
		"METHOD":method
	}
	res_body = appinfo(env,start_response)
	res_request_data = response_head + res_body
	res_request_data = res_request_data.encode('utf-8')
		
	ret = client_sock.send(res_request_data)	
	print('ret = %d'%ret)		
	client_sock.close()	


if __name__ == '__main__':
	main()
