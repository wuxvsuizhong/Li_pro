#!coding=utf-8

from socket import *
from multiprocessing import Process
import sys 
import re

normal_res = '''
	HTTP/1.1 200 OK\r\n
	\r\n
'''

error_res='''
	HTTP/1.1 404 NOT FOUND\r\n
	\r\n
	<body>
	<h1>file not found!<h1>
	</body>
'''



res_data = "Welcome!"

res_data= normal_res+res_data


HTTP_ROOT_DIR = "."



def main():
	#创建socket
	s = socket(AF_INET,SOCK_STREAM)
	#s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	try:
		s.bind(("",8000))
	except OSError as err:
		print('please wait %s'%str(err))
		sys.exit()

	s.listen(100)
	while True:
		client_sock,client_info = s.accept()
		print('new connection%s'%str(client_info))
		client_Process = Process(target = doserver,args=(client_sock,client_info))
		client_Process.start()
		client_sock.close()		
	s.close()


def doserver(client_sock,client_info):
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
    print('request file mame is %s'%str(file_name))

    if "/" == file_name:
        res_request_data = res_data.encode('utf-8')#返回默认响应
    elif file_name.endswith(".py"):
        #客户端请求执行脚本文件
        #执行脚本
        pass
    else:
        #返回请求响应数据_静态文件
        try:
            print("{}{}".format(HTTP_ROOT_DIR,file_name))
            with open(HTTP_ROOT_DIR+file_name,'r') as read_data:
                    request_data = read_data.read()+'\r\n'
        except IOError as err:
            print('file error '+str(err))
            res_request_data = error_res.encode('utf-8')
        else:
            #client_sock.send(normal_res)
            res_request_data = normal_res.encode('utf-8')+request_data.encode('utf-8')
	    
    ret = client_sock.send(res_request_data)	
    print('ret = %d'%ret)		
    client_sock.close()	


if __name__ == '__main__':
	main()
